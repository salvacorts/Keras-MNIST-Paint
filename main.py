#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image, ImageTk
from modules.load import Model
import modules.train as Trainer
from threading import Thread
import time


class Paint(object):

    DEFAULT_PEN_SIZE = 9.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("MINST Predictor")
        self.root.resizable(0,0)

        self.model = Model()


        self.brush_button = Button(self.root, text='Predict', command=self.Predict)
        self.brush_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='Clear', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg='white', width=150, height=150)
        self.c.grid(row=1, columnspan=5)

        self.predictionLabel = Text(self.root, fg='blue', height=1, width=30,
                                            borderwidth=0, highlightthickness=0,
                                            relief='ridge')
        self.predictionLabel.grid(row=0, column=6)

        self.predictionScores = Text(self.root, height=10, width=30, padx=10,
                                        borderwidth=0, highlightthickness=0,
                                        relief='ridge')
        self.predictionScores.grid(row=1, column=6)

        self.image = Canvas(self.root, width=150, height=150,
                                highlightthickness=0, relief='ridge')
        self.image.create_image(0, 0, anchor=NW, tags="IMG")
        self.image.grid(row=2, rowspan=5, columnspan=5)

        self.nnImageOriginal = Image.open("images/nn.png")
        self.resizeAndSetImage(self.nnImageOriginal)

        self.author = Label(self.root, text="@salvacorts")
        self.author.grid(row=3, column=6)

        self.info = Text(self.root, fg="red", height=2, width=20, borderwidth=0,
                            highlightthickness=0, relief='ridge')
        self.info.grid(row=4, column=6)


        self.trainButton = Button(self.root, fg="red", text="Train!", command=self.train)
        self.trainButton.grid(row=5, column=6)

        self.setup()
        self.root.mainloop()

    def train(self):
        Trainer.train()

    def resizeAndSetImage(self, image):
        size = (150, 150)
        resized = image.resize(size, Image.ANTIALIAS)
        self.nnImage = ImageTk.PhotoImage(resized)
        self.image.delete("IMG")
        self.image.create_image(0, 0, image=self.nnImage, anchor=NW, tags="IMG")

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.DEFAULT_PEN_SIZE
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def Predict(self):
        self.c.postscript(file="tmp.ps")
        img = Image.open("images/tmp.ps")
        img.save("images/out.png", "png")

        prediction, scores = self.model.Predict("images/out.png")

        self.predictionLabel.delete(1.0, END)
        self.predictionScores.delete(1.0, END)

        img = Image.open("images/current.png")
        self.resizeAndSetImage(img)

        n = 0
        self.predictionLabel.insert(END, "This is a {}".format(prediction))
        for score in scores:
            self.predictionScores.insert(END, "{}: {}\n".format(n, score))
            n += 1

    def use_eraser(self):
        self.predictionLabel.delete(1.0, END)
        self.predictionScores.delete(1.0, END)
        self.c.delete("all")
        self.resizeAndSetImage(self.nnImageOriginal)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.DEFAULT_PEN_SIZE
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    ge = Paint()
