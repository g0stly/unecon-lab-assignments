import tkinter
from tkinter import messagebox
from winsound import *
from datetime import *
from PIL import Image, ImageTk


class Clock:

    def __init__(self):

        self.mode = 'clock'
        self.alarm_time = None  # установленное время будильника
        self.stop_time = None  # время, при котором был включен режим установки будильника
        self.init_time = datetime.strftime(datetime.now(), '%H:%M')  # время при первом запуске часов
        self.flag = 0  # костыль: чтобы лишняя минута не накидывалась сходу после запуска (срабатывает after_idle)
        self.height = 241
        self.width = 430

        self.main_window = tkinter.Tk()
        self.main_window.title('digital clock')
        self.main_window.resizable(False, False)
        self.main_window.geometry('+960+340')

        self.canvas = tkinter.Canvas(self.main_window, height=self.height, width=self.width)
        self.canvas.pack()

        self.path = 'C:\\Users\\busya\\PycharmProjects\\питоню\\1 - по универу\\лаба 1 (гэу - 2019)\\design\\bg1.jpg'
        self.background_image = ImageTk.PhotoImage(Image.open(self.path))
        self.background_label = tkinter.Label(self.main_window, image=self.background_image)
        self.background_label.image = self.background_image
        self.background_label.place(x=0, y=0, relheight=1, relwidth=1)

        self.clk_frame = tkinter.Frame(self.main_window)
        self.clk_frame.place(relx=0.123, rely=0.15, relwidth=0.75, relheight=0.46)

        self.clk_label = tkinter.Label(self.clk_frame, font=('Digital-7', 115), bg='#F5FFFA', text=self.init_time)
        self.clk_label.place(relwidth=1, relheight=1)

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H',
                                    font=('Digital-7', 33), bd=3, command=lambda: self.lbl_config(60))
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M',
                                    font=('Digital-7', 33), bd=3, command=lambda: self.lbl_config(1))
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A',
                                    font=('Digital-7', 33), bd=3, command=self.alarm)

        self.h_btn.place(relx=0.06, rely=0.75, relwidth=0.2, relheight=0.2)
        self.m_btn.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.2)
        self.a_btn.place(relx=0.74, rely=0.75, relwidth=0.2, relheight=0.2)

        self.clk_label.after_idle(self.tick)
        self.main_window.mainloop()

    def tick(self):

        if self.flag == 1:
            self.init_time = str(datetime.strptime(self.init_time, '%H:%M') + timedelta(minutes=1))[11:16]
            self.clk_label.config(text=self.init_time)

            #if self.init_time == self.alarm_time:  # все сразу крашится, но музыка идет
            #    wake_up()
        else:
            self.flag = 1

        self.clk_label.after(60 * 10 ** 3, self.tick)

    def lbl_config(self, delta):

        if delta == 60:
            self.init_time = str(datetime.strptime(self.init_time, '%H:%M') + timedelta(minutes=delta))[11:16]
        else:
            self.init_time = self.init_time[:2] + \
                             str(datetime.strptime(self.init_time[3:], '%M') + timedelta(minutes=delta))[13:16]

        self.clk_label.config(text=self.init_time)

    def alarm(self):

        if self.mode == 'clock':
            self.stop_time = self.init_time
            self.mode = 'set alarm'
        else:
            self.alarm_time = self.init_time
            self.init_time = self.stop_time
            self.clk_label.config(text=self.init_time)
            self.mode = 'clock'
            messagebox.showinfo('info', f'The alarm was set for {self.alarm_time}')


def wake_up():

    filename = r'C:\Users\busya\PycharmProjects\питоню\1 - по универу\лаба 1 (гэу - 2019)\music.wav'
    PlaySound(filename, SND_FILENAME)


if __name__ == '__main__':
    test = Clock()
