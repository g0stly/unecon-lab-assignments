import tkinter
from PIL import Image, ImageTk


class Clock:

    def __init__(self):

        self.height = 241
        self.width = 430

        self.main_window = tkinter.Tk()
        self.main_window.title('digital clock')
        self.main_window.resizable(False, False)

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

        self.h_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='H', font=('Digital-7', 33), bd=3)
        self.m_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='M', font=('Digital-7', 33), bd=3)
        self.a_btn = tkinter.Button(self.main_window, bg='Misty Rose', text='A', font=('Digital-7', 33), bd=3)

        self.h_btn.place(relx=0.06, rely=0.75, relwidth=0.2, relheight=0.2)
        self.m_btn.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.2)
        self.a_btn.place(relx=0.74, rely=0.75, relwidth=0.2, relheight=0.2)

        self.main_window.mainloop()


if __name__ == '__main__':
    test = Clock()