import tkinter
import time


class Clock:

    def __init__(self):

        self.main_window = tkinter.Tk()
        self.main_window.title('Clock')
        self.main_window.resizable(False, False)

        self.clk_label = tkinter.Label(self.main_window, width=7, font=('Ubuntu', 95), bg='light cyan', text='00:00:00')
        self.clk_label.grid(row=0, columnspan=3)

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H')
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M')
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A')

        self.h_btn.grid(row=1, column=0, sticky='ew')
        self.m_btn.grid(row=1, column=1, sticky='ew')
        self.a_btn.grid(row=1, column=2, sticky='ew')

        self.clk_label.after_idle(self.tick)
        tkinter.mainloop()

    def tick(self):
        # впоследствии поменять время обновления на 60*10^3 и убрать секунды (+ изменить ширину окна)
        self.clk_label.config(text=time.strftime('%H:%M:%S'))
        self.clk_label.after(200, self.tick)


if __name__ == '__main__':
    test = Clock()
