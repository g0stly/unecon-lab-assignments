import tkinter
import time


class Clock:
    # подумать, куда засунуть исходное время(списать у )
    current_time = '23:00'

    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title('Clock')
        self.main_window.resizable(False, False)

        self.clk_label = tkinter.Label(self.main_window, width=7, font=('Ubuntu', 95), bg='light cyan', text=Clock.current_time)
        self.clk_label.grid(row=0, columnspan=3)

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H', command=self.tick(60))
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M', command=self.tick(1))
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A')

        self.h_btn.grid(row=1, column=0, sticky='ew')
        self.m_btn.grid(row=1, column=1, sticky='ew')
        self.a_btn.grid(row=1, column=2, sticky='ew')

        self.clk_label.after_idle(self.tick(1))
        tkinter.mainloop()
    
    # переписать две эти функции
    # добавить аргумент, который, в зависимости от значения, запускает рекурсию или не запускает
    # 
    
    def tick(self, incr=1):
        # впоследствии поменять время обновления на 60*10^3 и убрать секунды (+ изменить ширину окна)
        #global Clock.current_time
        Clock.current_time = self.incr(Clock.current_time, incr)
        self.clk_label.config(text=Clock.current_time)
        self.clk_label.after(200, self.tick)

    def incr(self, current_time, increment=1):

        hours = current_time[:2]
        minutes = current_time[3:]

        if minutes == '59':
            if hours == '23':
                hours = '00'
            else:
                hours = str(int(hours) + 1)
                if len(hours) == 1:
                    hours = '0' + hours
            minutes = '00'
        else:
            minutes = str(int(minutes) + 1)
            if len(minutes) == 1:
                minutes = '0' + minutes
        return hours + ':' + minutes



if __name__ == '__main__':
    
    test = Clock()
