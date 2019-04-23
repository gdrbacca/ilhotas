import tkfilebrowser
from tkinter import *
from PIL import ImageTk, Image
import imutils
import cv2
import os
import main
import utils

class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack(fill=BOTH, pady=15)
        self.abrir = Button(self.widget1)
        self.abrir["text"] = "Abrir imagem"
        self.abrir["font"] = ("Verdana", "10")
        self.abrir["width"] = 10
        self.abrir["command"] = self.abrirImagem
        self.abrir.pack(side=LEFT, padx=20)
        self.labelcaminho = Label(self.widget1, text="Caminho da imagem: ")
        self.labelcaminho.pack(side=LEFT)
        self.caminho = Label(self.widget1)
        self.caminho.pack(side=LEFT, fill=X)

        self.widget2 = Frame(master)
        self.widget2.pack()
        self.image1 = Image.open("no-image.png")
        self.image2 = ImageTk.PhotoImage(self.image1)
        self.img = Label(self.widget2, image=self.image2)
        self.img.grid(row=0, column=0)

        self.widget3 = Frame(self.widget2)
        self.widget3.grid(row=0, column=1, padx=10)
        self.a = Button(self.widget3)
        self.a["text"] = "Abrir imagem"
        self.a["font"] = ("Verdana", "10")
        self.a["width"] = 10
        self.a.grid(row=3, column=1, columnspan=2)
        self.info1Label = Label(self.widget3)
        self.info1Label["text"] = "info1: "
        self.info1Label["width"] = 10
        self.info1Label.grid(row=0, column=0)
        self.info1 = Label(self.widget3)
        self.info1["text"] = "o"
        self.info1["width"] = 15
        self.info1.grid(row=0, column=1)
        self.info2Label = Label(self.widget3)
        self.info2Label["text"] = "info2: "
        self.info2Label["width"] = 10
        self.info2Label.grid(row=1, column=0)
        self.info2 = Label(self.widget3)
        self.info2["text"] = "e"
        self.info2["width"] = 15
        self.info2.grid(row=1, column=1)


    def abrirImagem(self):
        #filename = tkfilebrowser.askopenfilename()
        #if filename != "":

        #img = Image.open(filename)
        #img = cv2.imread(filename, 1)
        #img = imutils.resize(img, height=500)
        m = main.Main()
        u = utils.Segment()
        filename = tkfilebrowser.askopenfilename()
        if filename != "":
            img = m.leImagem(filename)
            image = Image.fromarray(img)
            image = ImageTk.PhotoImage(image)
            self.caminho["text"] = filename
            self.img.configure(image=image)
            self.img.image = image
            root.update()
            img = m.processaImagem(filename, []) #cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if img != []:
                print(img.shape[0], ' ', img.shape[1])
                image = Image.fromarray(img)
                image = ImageTk.PhotoImage(image)
                self.img.configure(image=image)
                self.img.image = image
                print("dsdsdsdsds")

    def mudarTexto(self):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"
        else:
            self.msg["text"] = "Primeiro widget"

root = Tk()
Application(root)
root.mainloop()