import tkfilebrowser
from tkinter import *
from PIL import ImageTk, Image
import imutils
import cv2
import os
import main
import utils

class Application:

    thresh1 = 240
    thresh2 = 160
    thresh3 = 150
    filename = ""
    areaEscala = 0
    primeiroThresh = False
    result1 = []
    original = []

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
        self.img.grid(row=0, column=0, rowspan=2)

        self.widget3 = Frame(self.widget2)
        self.widget3.grid(row=0, column=1)
        self.a = Button(self.widget3)
        self.a["text"] = "Primeiro limiar"
        self.a["font"] = ("Verdana", "10")
        self.a["width"] = 12
        self.a["command"] = self.processamento
        self.a.grid(row=3, column=1, sticky=W+E)

        self.buttonThresh1a = Button(self.widget3)
        self.buttonThresh1a["text"] = "-"
        self.buttonThresh1a["width"] = 5
        self.buttonThresh1a["command"] = self.diminuiThresh1
        self.buttonThresh1a.grid(row=0, column=0)
        self.info1 = Label(self.widget3)
        self.info1["text"] = self.thresh1
        self.info1["width"] = 10
        self.info1.grid(row=0, column=1)
        self.buttonThresh1b = Button(self.widget3)
        self.buttonThresh1b["text"] = "+"
        self.buttonThresh1b["width"] = 5
        self.buttonThresh1b["command"] = self.maisThresh1
        self.buttonThresh1b.grid(row=0, column=2)
        self.buttonThresh2a = Button(self.widget3)
        self.buttonThresh2a["text"] = "-"
        self.buttonThresh2a["width"] = 5
        self.buttonThresh2a["command"] = self.diminuiThresh2
        self.buttonThresh2a.grid(row=1, column=0)
        self.info2 = Label(self.widget3)
        self.info2["text"] = self.thresh2
        self.info2["width"] = 10
        self.info2.grid(row=1, column=1)
        self.buttonThresh2b = Button(self.widget3)
        self.buttonThresh2b["text"] = "+"
        self.buttonThresh2b["width"] = 5
        self.buttonThresh2b["command"] = self.maisThresh2
        self.buttonThresh2b.grid(row=1, column=2)

        self.espaco = Label(self.widget3)
        self.espaco.grid(row=4, column=1)

        self.b = Button(self.widget3)
        self.b["text"] = "Segundo limiar"
        self.b["font"] = ("Verdana", "10")
        self.b["width"] = 12
        self.b['state'] = 'disabled'
        self.b["command"] = self.processamento2
        self.b.grid(row=6, column=1)
        self.buttonThresh3a = Button(self.widget3)
        self.buttonThresh3a["text"] = "-"
        self.buttonThresh3a["width"] = 5
        self.buttonThresh3a["command"] = self.diminuiThresh3
        self.buttonThresh3a["state"] = 'disabled'
        self.buttonThresh3a.grid(row=5, column=0)
        self.info3 = Label(self.widget3)
        self.info3["text"] = self.thresh3
        self.info3["width"] = 12
        self.info3.grid(row=5, column=1)
        self.buttonThresh3b = Button(self.widget3)
        self.buttonThresh3b["text"] = "+"
        self.buttonThresh3b["width"] = 5
        self.buttonThresh3b["command"] = self.maisThresh3
        self.buttonThresh3b["state"] = 'disabled'
        self.buttonThresh3b.grid(row=5, column=2)

        self.widget4 = Frame(self.widget2)
        self.widget4.grid(row=1, column=1, sticky=N)
        self.areaIlhotaText = Label(self.widget4)
        self.areaIlhotaText["text"] = 'Área: '
        self.areaIlhotaText["width"] = 10
        self.areaIlhotaText.grid(row=0, column=0)
        self.areaIlhota = Label(self.widget4)
        self.areaIlhota["text"] = self.areaEscala
        self.areaIlhota["width"] = 10
        self.areaIlhota.grid(row=0, column=1, columnspan=2, pady=10)
        self.circularidadeText = Label(self.widget4)
        self.circularidadeText["text"] = 'Circular: '
        self.circularidadeText["width"] = 10
        self.circularidadeText.grid(row=1, column=0)
        self.circularidade = Label(self.widget4)
        self.circularidade["text"] = self.areaEscala
        self.circularidade["width"] = 10
        self.circularidade.grid(row=1, column=1, columnspan=2, pady=10)
        self.perimetroText = Label(self.widget4)
        self.perimetroText["text"] = 'Perímetro: '
        self.perimetroText["width"] = 10
        self.perimetroText.grid(row=2, column=0)
        self.perimetro = Label(self.widget4)
        self.perimetro["text"] = self.areaEscala
        self.perimetro["width"] = 10
        self.perimetro.grid(row=2, column=1, columnspan=2, pady=10)

    def diminuiThresh1(self):
        self.thresh1 -= 5
        self.info1["text"] = self.thresh1

    def maisThresh1(self):
        self.thresh1 += 5
        self.info1["text"] = self.thresh1

    def maisThresh2(self):
        self.thresh2 += 5
        self.info2["text"] = self.thresh2

    def diminuiThresh2(self):
        self.thresh2 -= 5
        self.info2["text"] = self.thresh2
        print(self.thresh2)

    def maisThresh3(self):
        self.thresh3 += 5
        self.info3["text"] = self.thresh3

    def diminuiThresh3(self):
        self.thresh3 -= 5
        self.info3["text"] = self.thresh3

    def processamento(self):
        m = main.Main()
        if self.filename != "":
            img = m.leImagem(self.filename)
            image = Image.fromarray(img)
            image = ImageTk.PhotoImage(image)
            self.caminho["text"] = "Carregando..."
            root.update()
            self.img.configure(image=image)
            self.img.image = image
            if self.filename == "" or self.caminho["text"] == "Carregando...":
                root.update()
            self.areaEscala, img = m.processaImagem(self.filename, [], self.thresh1, self.thresh2) #cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            print('escala: ', self.areaEscala)
            self.caminho["text"] = self.filename
            self.b['state'] = 'normal'
            self.buttonThresh3a['state'] = 'normal'
            self.buttonThresh3b['state'] = 'normal'
            self.primeiroThresh = True
            #img = u.processa2(filename)
            if img != []:
                print(img.shape[0], ' ', img.shape[1])
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                image = Image.fromarray(img)
                image = ImageTk.PhotoImage(image)
                self.img.configure(image=image)
                self.img.image = image
                self.result1 = img
                print("dsdsdsdsds")

    def processamento2(self):
        if self.primeiroThresh == True:
            self.buttonThresh1a['state'] = 'disabled'
            self.buttonThresh1b['state'] = 'disabled'
            self.buttonThresh2a['state'] = 'disabled'
            self.buttonThresh2b['state'] = 'disabled'
            self.a['state'] = 'disabled'
            u = utils.Segment()
            self.caminho['text'] = "Carregando..."
            root.update()
            circularidade, area, contours, cont, image = u.processaFinal(self.result1, self.thresh3)
            size = 128, 128
            areaResult = area / self.areaEscala
            print('areaIlhota: ', area)
            if circularidade:
                self.circularidade["text"] = 'Sim'
            else:
                self.circularidade["text"] = 'Não'
            self.areaIlhota["text"] = ("%.2f" % areaResult)
            self.perimetro["text"] = ("%.2f" % cv2.arcLength(contours[cont], True))
            self.caminho['text'] = self.filename
            root.update()
            image = cv2.resize(image, dsize=(550, 500), interpolation=cv2.INTER_CUBIC)
            imagem = Image.fromarray(image)
            ima = imagem
            basewidth = 600
            wpercent = (basewidth / float(ima.size[0]))
            hesi = int(float(ima.size[1]) * float(wpercent))
            ima = ima.resize((basewidth, hesi), Image.ANTIALIAS)
            #ima.save('resized.jpg')
            #cv2.imwrite('results/im6.jpg', image)
            imagem1 = ImageTk.PhotoImage(ima)
            self.img.configure(image=imagem1)
            self.img.image = imagem1
            print('proc2')

    def abrirImagem(self):
        #filename = tkfilebrowser.askopenfilename()
        #if filename != "":

        #img = Image.open(filename)
        #img = cv2.imread(filename, 1)
        #img = imutils.resize(img, height=500)
        m = main.Main()
        u = utils.Segment()
        self.filename = tkfilebrowser.askopenfilename()
        self.a['state'] = 'normal'
        self.b['state'] = 'disabled'
        self.buttonThresh3a['state'] = 'disabled'
        self.buttonThresh3b['state'] = 'disabled'
        if self.filename != "":
            self.processamento()

    def mudarTexto(self):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"
        else:
            self.msg["text"] = "Primeiro widget"

root = Tk()
Application(root)
root.mainloop()