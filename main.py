import tkinter as tk
import time
from PIL import Image, ImageTk
import pygame as p

stopwatch_counter = 0
alarm_counter = 0


class Time:
    def __init__(self):
        self._current_time = time.localtime()

    # change the time
    def change_time(self):
        t = time.localtime()

        current_time = time.strftime("%I: %M", t)  # time is set in 12-hour clock

        if current_time[0] == "0":
            current_time = current_time[1:]
        # print(current_time)

        return current_time

    def change_seconds(self):
        seconds = time.strftime("%S")
        # print(seconds)

        return seconds

    def change_time_of_day(self):
        time_of_day = time.strftime("%p")
        # print(time_of_day)

        return time_of_day

    def change_current_date(self):
        current_date = time.strftime("%B %d, %Y")
        # print(current_date)

        return current_date

    def change_current_day(self):
        current_day = time.strftime("%A")
        # print(current_day)

        return current_day


class Stopwatch(Time):
    def __init__(self):
        super().__init__()
        self._time = Time()
        self._stopwatch_milliseconds_counter = 0
        self._stopwatch_seconds_counter = 1
        self._stopwatch_minutes_counter = 1

    def start_stopwatch(self):
        global stopwatch_counter
        if stopwatch_counter == 0:
            # print(self._stopwatch_counter)
            self._stopwatch_milliseconds_counter += 1

            stopwatch_milliseconds_counter_label.configure(text=self._stopwatch_milliseconds_counter)

            if self._stopwatch_milliseconds_counter == 95:
                self._stopwatch_milliseconds_counter = 0
                self.change_stopwatch_seconds()

            root.after(3, self.start_stopwatch)

        if stopwatch_counter == 1:
            stopwatch_counter = 0

    def pause_stopwatch(self):
        global stopwatch_counter
        stopwatch_counter = 1
        # root.after_cancel(self.start_stopwatch)

    def change_stopwatch_seconds(self):
        # print(self._stopwatch_minutes_counter)

        if self._stopwatch_seconds_counter == 60:
            self.change_stopwatch_minutes()
            self._stopwatch_seconds_counter = 0

        # check if the counter is more than 10 seconds (change text label accordingly)
        if self._stopwatch_seconds_counter >= 10:
            stopwatch_seconds_counter_label.configure(text=str(self._stopwatch_seconds_counter) + '.')
        else:
            stopwatch_seconds_counter_label.configure(text='0' + str(self._stopwatch_seconds_counter) + '.')

        self._stopwatch_seconds_counter += 1

    def change_stopwatch_minutes(self):
        if self._stopwatch_minutes_counter >= 10:
            stopwatch_minutes_counter_label.configure(text=str(self._stopwatch_minutes_counter) + ':')
        else:
            stopwatch_minutes_counter_label.configure(text='0' + str(self._stopwatch_minutes_counter) + ':')

        self._stopwatch_minutes_counter += 1

    def reset_stopwatch(self):
        self.pause_stopwatch()

        self._stopwatch_milliseconds_counter = 0
        self._stopwatch_seconds_counter = 1
        self._stopwatch_minutes_counter = 1

        stopwatch_milliseconds_counter_label.configure(text="00")
        stopwatch_seconds_counter_label.configure(text="00.")
        stopwatch_minutes_counter_label.configure(text="00:")


class Alarm(Time):
    def __init__(self):
        super().__init__()
        self._hours_input = 0
        self._minutes_input = 0
        self._seconds_input = 0
        self._alarm_counter = 0
        self._alarm_active = False

    def get_alarm_details(self):
        if self._alarm_active is False:
            try:
                temp = int(alarm_entry.get())

                if temp < 0:
                    print("Please enter a positive whole number! ")
                    return

                if temp >= 60:
                    print("Please enter a whole number less than 60! ")
                    return

            except ValueError:
                print("Please enter a whole number! ")
                return

            if self._alarm_counter == 0:
                self._hours_input = alarm_entry.get()

                self._alarm_counter = 1
                prompt_label.configure(text="Enter minutes ->")
                # print(self._hours_input)

                alarm_entry.delete(0, 'end')
                return

            if self._alarm_counter == 1:
                self._minutes_input = alarm_entry.get()

                self._alarm_counter = 2
                prompt_label.configure(text="Enter seconds ->")
                # print(self._minutes_input)

                alarm_entry.delete(0, 'end')
                return

            if self._alarm_counter == 2:
                self._seconds_input = alarm_entry.get()

                self._alarm_counter = 0
                prompt_label.configure(text="Alarm active...")
                # print(self._seconds_input)

                if int(self._hours_input) < 10:
                    self._hours_input = '0' + self._hours_input

                if int(self._minutes_input) < 10:
                    self._minutes_input = '0' + self._minutes_input

                if int(self._seconds_input) < 10:
                    self._seconds_input = '0' + self._seconds_input

                alarm_label.configure(text=self._hours_input + ':' + self._minutes_input + ':' + self._seconds_input)
                self._alarm_active = True

                alarm_entry.delete(0, 'end')

                self.change_alarm_seconds()

        else:
            print("An alarm is still active! Consider waiting or resetting...")

    def change_alarm_seconds(self):
        global alarm_counter
        if alarm_counter == 0:
            if int(self._seconds_input) == -1 and int(self._minutes_input) == 0 and int(self._hours_input) == 0:
                self.reset_alarm()

                p.mixer.init()
                p.mixer.music.load("alarm_sound.mp3")
                p.mixer.music.play(loops=0)

            if int(self._seconds_input) == -1:
                self.change_alarm_minutes()
                self._seconds_input = '59'

            # check if seconds is more than 10 (change text label accordingly)
            if int(self._seconds_input) < 10:
                self._seconds_input = '0' + str(self._seconds_input)
            else:
                self._seconds_input = str(self._seconds_input)

            if len(str(self._seconds_input)) == 3:
                self._seconds_input = str(self._seconds_input[1:])

            if len(str(self._minutes_input)) == 1:
                self._minutes_input = '0' + str(self._minutes_input)

            if len(str(self._hours_input)) == 1:
                self._hours_input = '0' + str(self._hours_input)

            alarm_label.configure(text=str(self._hours_input) + ':' + str(self._minutes_input) + ':' +
                                       str(self._seconds_input))

            self._seconds_input = int(self._seconds_input) - 1

            root.after(1000, self.change_alarm_seconds)

    def change_alarm_minutes(self):
        if int(self._minutes_input) == 0:
            self._change_alarm_hours()
            self._minutes_input = '60'

        if int(self._minutes_input) < 10:
            self._minutes_input = '0' + str(self._minutes_input)
        else:
            self._minutes_input = str(self._minutes_input)

        alarm_label.configure(text=str(self._hours_input) + ':' + str(self._minutes_input) + ':' +
                                   str(self._seconds_input))

        self._minutes_input = int(self._minutes_input) - 1

    def _change_alarm_hours(self):
        if int(self._hours_input) == 0:
            self._hours_input = '0'

        if int(self._hours_input) < 10:
            self._hours_input = '0' + str(self._hours_input)
        else:
            self._hours_input = str(self._hours_input)

        self._hours_input = int(self._hours_input) - 1

        alarm_label.configure(text=str(self._hours_input) + ':' + str(self._minutes_input) + ':' +
                                   str(self._seconds_input))

    def pause_alarm(self):
        if self._alarm_active is True:
            global alarm_counter
            if alarm_counter == 1:
                alarm_counter = 0
                pause_alarm_pic = ImageTk.PhotoImage(Image.open("pause_alarm_pic.PNG").resize((75, 75)))
                alarm_pause_resume_button_label.configure(image=pause_alarm_pic)
                alarm_pause_resume_button_label.image = pause_alarm_pic
                self.change_alarm_seconds()
            else:
                alarm_counter = 1
                resume_alarm_pic = ImageTk.PhotoImage(Image.open("resume_alarm_pic.PNG").resize((75, 75)))
                alarm_pause_resume_button_label.configure(image=resume_alarm_pic)
                alarm_pause_resume_button_label.image = resume_alarm_pic
        else:
            print("Alarm has not been set yet! ")

    def reset_alarm(self):
        self.pause_alarm()

        self._seconds_input = 0
        self._minutes_input = 0
        self._hours_input = 0

        self._alarm_counter = 0
        self._alarm_active = False

        alarm_label.configure(text="00:00:00")
        prompt_label.configure(text="Enter hours ->")


class TimeGUI:
    def __init__(self, root):
        self._backend = Time()
        s = Stopwatch()
        a = Alarm()

        root.title("Time")
        root.configure(background='#3F5F89')
        root.geometry('1024x768')

        black_border_clock = ImageTk.PhotoImage(Image.open("border.PNG").resize((700, 320)))
        black_border_clock_label = tk.Label(root, image=black_border_clock, borderwidth=0, highlightthickness=0)
        black_border_clock_label.place(x=150, y=75)

        current_time = self._backend.change_time()
        self._time_string = tk.Label(text=current_time)
        self._time_string.config(font=("Segoe Print", 80), fg="black", bg="#3F5F89")
        self._time_string.place(x=260, y=125)

        seconds = self._backend.change_seconds()
        self._seconds_string = tk.Label(text=seconds)
        self._seconds_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._seconds_string.place(x=650, y=220)

        current_time_of_day = self._backend.change_time_of_day()
        self._time_of_day_string = tk.Label(text=current_time_of_day)
        self._time_of_day_string.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        self._time_of_day_string.place(x=690, y=85)

        current_date = self._backend.change_current_date()
        self._date_string = tk.Label(text=current_date)
        self._date_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._date_string.place(x=200, y=300)

        current_day = self._backend.change_current_day()
        self._day_string = tk.Label(text=current_day)
        self._day_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._day_string.place(x=635, y=300)

        black_border_stopwatch = ImageTk.PhotoImage(Image.open("border.PNG").resize((400, 300)))
        black_border_stopwatch_label = tk.Label(root, image=black_border_stopwatch, borderwidth=0, highlightthickness=0)
        black_border_stopwatch_label.place(x=100, y=425)

        stopwatch_start_button = ImageTk.PhotoImage(Image.open("play_button_pic.PNG").resize((75, 75)))
        stopwatch_start_button_label = tk.Button(image=stopwatch_start_button, command=s.start_stopwatch, borderwidth=0)
        stopwatch_start_button_label.place(x=140, y=610)

        stopwatch_pause_button = ImageTk.PhotoImage(Image.open("pause_button_pic.PNG").resize((75, 75)))
        stopwatch_pause_button_label = tk.Button(image=stopwatch_pause_button, command=s.pause_stopwatch, borderwidth=0)
        stopwatch_pause_button_label.place(x=260, y=610)

        stopwatch_reset_button = ImageTk.PhotoImage(Image.open("reset_button_pic.PNG").resize((75, 75)))
        stopwatch_reset_button_label = tk.Button(image=stopwatch_reset_button, command=s.reset_stopwatch, borderwidth=0)
        stopwatch_reset_button_label.place(x=380, y=610)

        global stopwatch_milliseconds_counter_label
        stopwatch_milliseconds_counter_label = tk.Label(text="00")
        stopwatch_milliseconds_counter_label.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        stopwatch_milliseconds_counter_label.place(x=355, y=475)

        global stopwatch_seconds_counter_label
        stopwatch_seconds_counter_label = tk.Label(text="00.")
        stopwatch_seconds_counter_label.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        stopwatch_seconds_counter_label.place(x=255, y=475)

        global stopwatch_minutes_counter_label
        stopwatch_minutes_counter_label = tk.Label(text="00:")
        stopwatch_minutes_counter_label.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        stopwatch_minutes_counter_label.place(x=155, y=475)

        black_border_alarm = ImageTk.PhotoImage(Image.open("border.PNG").resize((400, 300)))
        black_border_alarm_label = tk.Label(root, image=black_border_alarm, borderwidth=0, highlightthickness=0)
        black_border_alarm_label.place(x=500, y=425)

        global alarm_label
        alarm_label = tk.Label(text="00:00:00")
        alarm_label.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        alarm_label.place(x=565, y=475)

        alarm_cancel_button = ImageTk.PhotoImage(Image.open("cancel_alarm_pic.PNG").resize((75, 75)))
        alarm_cancel_button_label = tk.Button(image=alarm_cancel_button, command=a.reset_alarm, borderwidth=0)
        alarm_cancel_button_label.place(x=580, y=610)

        global alarm_pause_resume_button_label
        alarm_pause_resume_button = ImageTk.PhotoImage(Image.open("pause_alarm_pic.PNG").resize((75, 75)))
        alarm_pause_resume_button_label = tk.Button(image=alarm_pause_resume_button, command=a.pause_alarm,
                                                    borderwidth=0)
        alarm_pause_resume_button_label.place(x=740, y=610)

        global prompt_label
        prompt_label = tk.Label(text="Enter hours -> ")
        prompt_label.config(font=("Courier", 14))
        prompt_label.place(x=560, y=575)

        global alarm_entry
        alarm_entry = tk.Entry(bd=3, width=2, font="Calibri 20")
        alarm_entry.place(x=748, y=574, height=30)

        enter_button = tk.Button(bd=5, width=5, text="Enter", command=a.get_alarm_details)
        enter_button.place(x=785, y=575, height=30)

        self.update_clock_details()

        root.mainloop()

    def update_clock_details(self):
        self._time_string.configure(text=self._backend.change_time())
        self._seconds_string.configure(text=self._backend.change_seconds())
        self._time_of_day_string.configure(text=self._backend.change_time_of_day())
        self._date_string.configure(text=self._backend.change_current_date())
        self._day_string.configure(text=self._backend.change_current_day())

        root.after(500, self.update_clock_details)


if __name__ == "__main__":
    root = tk.Tk()
    c = TimeGUI(root)
