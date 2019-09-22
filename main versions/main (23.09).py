import tkinter
from datetime import *


class Clock:

    def __init__(self):

        self.mode = 1
        self.init_time = datetime.strftime(datetime.now(), '%H:%M')

        self.main_window = tkinter.Tk()
        self.main_window.title('Clock')
        self.main_window.resizable(False, False)

        self.clk_label = tkinter.Label(self.main_window, width=7, font=('Ubuntu', 95),
                                       bg='light cyan', text=self.init_time)
        self.clk_label.grid(row=0, columnspan=3)

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H', command=lambda: self.lbl_config(60))
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M', command=lambda: self.lbl_config(1))
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A')

        self.h_btn.grid(row=1, column=0, sticky='ew')
        self.m_btn.grid(row=1, column=1, sticky='ew')
        self.a_btn.grid(row=1, column=2, sticky='ew')

        self.clk_label.after_idle(self.tick)
        tkinter.mainloop()

    def tick(self):

        self.init_time = str(datetime.strptime(self.init_time, '%H:%M') + timedelta(minutes=1))[11:16]
        self.clk_label.config(text=self.init_time)
        self.clk_label.after(60 * 10 ** 3, self.tick)

    def lbl_config(self, delta):

        if delta == 60:
            self.init_time = str(datetime.strptime(self.init_time, '%H:%M') + timedelta(minutes=delta))[11:16]
        else:
            self.init_time = self.init_time[:2] + \
                             str(datetime.strptime(self.init_time[3:], '%M') + timedelta(minutes=delta))[13:16]

        self.clk_label.config(text=self.init_time)


if __name__ == '__main__':
    test = Clock()
