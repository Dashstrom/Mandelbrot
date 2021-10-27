from mandelbrot.view.base import AdjustableInput
from tkinter import *
from typing import Any, Dict, Optional
from mandelbrot.utils import resource_path
from tkinter.ttk import Progressbar
from math import ceil
from PIL import Image, ImageTk
from time import sleep
from tkinter.filedialog import asksaveasfilename


class Wait(Toplevel):
    def __init__(self, view: Optional[Misc]) -> None:
        super().__init__(view)
        self.resizable(width=False, height=False)
        self.title("Opération lente")
        self.root = view
        self.configure()
        self.geometry("300x300")
        try:
            self.iconbitmap(resource_path("logo.ico"))
        except Exception as err:
            print(err)

        self.__image = None
        self.__image_tk = None
        self.__index = None
        self.var = IntVar(self, 0)

        self.label = Label(self, text="Une opération lente est en cours")
        self.canvas = Canvas(self, width=200, height=200, bd=0,
                             highlightthickness=0, bg="#c8c8c8")
        self.progressbar = Progressbar(self, variable=self.var,
                                       orient=HORIZONTAL, value=0, maximum=100)
        self.ok = Button(self, text="Done bitch")

        self.label.pack(fill=X, padx=20)
        self.canvas.pack()
        self.progressbar.pack(fill=X, side=BOTTOM)
        self.ok.pack(padx=20)

        self.take_control()

    def done(self):
        self.destroy()

    def set_preview(self, image: Image.Image):
        w, h = image.size
        ratio_w = w / 200
        ratin_h = h / 200
        ratio = max(ratin_h, ratio_w)
        img_w = ceil(w / ratio)
        img_h = ceil(h / ratio)
        self.__image = image.resize((img_w, img_h))
        self.__image_tk = ImageTk.PhotoImage(self.__image)
        if self.__index is not None:
            self.canvas.delete(self.__index)
        self.__index = self.canvas.create_image(
            100 - img_w/2, 100 - img_h/2, image=self.__image_tk, anchor=NW)
        self.canvas.tag_lower(self.__index)
        self.update_idletasks()

    def progress(self, percent: float) -> None:
        if ceil(percent * 100) != self.var.get():
            self.var.set(ceil(percent * 100))
            self.root.update()
            self.root.update_idletasks()

    def take_control(self) -> None:
        self.transient(self.root)
        self.grab_set()
        # self.root.wait_window(self)