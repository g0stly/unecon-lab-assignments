import tkinter
from PIL import Image, ImageTk

path = 'C:\\Users\\busya\\PycharmProjects\\питоню\\1 - по универу\\лаба 1 (гэу - 2019)\\design\\bg1.jpg'

root = tkinter.Tk()
img = ImageTk.PhotoImage(Image.open(path))
panel = tkinter.Label(root, image=img, width=500, height=500)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()
