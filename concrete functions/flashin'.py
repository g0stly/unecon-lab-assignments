import tkinter
import time


def flashing():
    global test_str, k

    try:
        k
    except NameError:
        k = 0

    if k == 0:
        test_label.config(text='  :  ')
        k = 1
        test_label.after(350, flashing)
    else:
        test_label.config(text=test_str)
        k = 0
        test_label.after(350, flashing)


test_str = '13:15'
main_window = tkinter.Tk()

test_label = tkinter.Label(main_window, width=5,
                           font=('Ubuntu', 70), text=test_str)
test_label.grid(row=0, column=0)

test_btn = tkinter.Button(main_window, text='turn flashing on', command=flashing)
test_btn.grid(row=1, column=0)

tkinter.mainloop()
