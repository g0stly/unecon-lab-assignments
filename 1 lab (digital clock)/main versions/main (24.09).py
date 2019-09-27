import tkinter
from tkinter import messagebox
from winsound import *
from datetime import *
from PIL import Image, ImageTk


class Clock:

    def __init__(self):

        self.mode = 'clock'
        self.alarm_time = None  # установленное время будильника
        self.stop_time = None  # время, при котором был включен режим часов
        self.init_time = datetime.strftime(datetime.now(), '%H:%M')  # время при первом запуске часов
        self.flag = 0  # костыль: чтобы лишняя минута не накидывалась сходу после запуска (срабатывает after_idle)

        self.main_window = tkinter.Tk()
        self.main_window.title('digital clock')
        self.main_window.resizable(False, False)

        #load = Image.open(
        # 'C:\\Users\\busya\\PycharmProjects\\питоню\\1 - по универу\\лаба 1 (гэу - 2019)\\design\\bg1.jpg')
        #render = ImageTk.PhotoImage(load)

        self.clk_label = tkinter.Label(self.main_window, width=6, font=('Ubuntu', 95),
                                       bg='light cyan', text=self.init_time)#, image=render)
        self.clk_label.grid(row=0, columnspan=3)

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H', command=lambda: self.lbl_config(60))
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M', command=lambda: self.lbl_config(1))
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A', command=self.alarm)

        self.h_btn.grid(row=1, column=0, sticky='ew')
        self.m_btn.grid(row=1, column=1, sticky='ew')
        self.a_btn.grid(row=1, column=2, sticky='ew')

        self.clk_label.after_idle(self.tick)
        tkinter.mainloop()

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

