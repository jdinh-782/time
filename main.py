import tkinter as tk
import time
from PIL import Image, ImageTk


class Clock:
    def __init__(self):
        self._current_time = time.localtime()

    # change the time
    def change_time(self):
        t = time.localtime()

        current_time = time.strftime("%I:%M", t)  # time is set in 12-hour clock

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

class ClockGUI:
    def __init__(self, root):
        self._backend = Clock()

        root.title("Time")
        root.configure(background='#3F5F89')
        root.geometry('1024x768')

        black_border_pic = ImageTk.PhotoImage(Image.open("border.PNG").resize((700, 320)))
        black_border_pic_label = tk.Label(root, image=black_border_pic, borderwidth=0, highlightthickness=0)
        black_border_pic_label.place(x=150, y=150)

        current_time = self._backend.change_time()
        self._time_string = tk.Label(text=current_time)
        self._time_string.config(font=("Segoe Print", 80), fg="black", bg="#3F5F89")
        self._time_string.place(x=300, y=200)

        seconds = self._backend.change_seconds()
        self._seconds_string = tk.Label(text=seconds)
        self._seconds_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._seconds_string.place(x=640, y=295)

        current_time_of_day = self._backend.change_time_of_day()
        self._time_of_day_string = tk.Label(text=current_time_of_day)
        self._time_of_day_string.config(font=("Segoe Print", 40), fg="black", bg="#3F5F89")
        self._time_of_day_string.place(x=690, y=160)

        current_date = self._backend.change_current_date()
        self._date_string = tk.Label(text=current_date)
        self._date_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._date_string.place(x=200, y=375)

        current_day = self._backend.change_current_day()
        self._day_string = tk.Label(text=current_day)
        self._day_string.config(font=("Segoe Print", 25), fg="black", bg="#3F5F89")
        self._day_string.place(x=635, y=375)

        self.update_details_string()

        root.mainloop()

    def update_details_string(self):
        self._time_string.configure(text=self._backend.change_time())
        self._seconds_string.configure(text=self._backend.change_seconds())
        self._time_of_day_string.configure(text=self._backend.change_time_of_day())
        self._date_string.configure(text=self._backend.change_current_date())
        self._day_string.configure(text=self._backend.change_current_day())

        root.after(250, self.update_details_string)


if __name__ == "__main__":
    root = tk.Tk()
    c = ClockGUI(root)
