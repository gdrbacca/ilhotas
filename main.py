import cv2
import numpy as np
import imutils
import tkfilebrowser
import utils
from sklearn.cluster import KMeans

class Main:

    contador = 0

    def leImagem(self, caminho):
        imagem = cv2.imread(caminho, 1)
        print(caminho)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        imagem = imutils.resize(imagem, height=500)
        return imagem


    def adjust_gamma(self, image, gamma):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def medeScala(self, imagem):
        img = imagem
        h, w = img.shape[:2]
        img = imutils.resize(img, width=666, height=500)
        h, w = img.shape[:2]
        #cv2.imshow('original', img)
        #cv2.imwrite('fff.jpg', img)
        print(h, ' ', w)
        # crop_img = img[y:y+h, x:x+w]
        crop_img = img[h - 50:h, w - 80:w]
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY, 1)
        ret, thresh = cv2.threshold(crop_img, 60, 255, cv2.THRESH_BINARY)
        cv2.imshow('rr', thresh)
        edges = cv2.Canny(thresh, 200, 500, None, 3)
        cv2.imshow("canny", edges)
        cv2.imwrite('edges1.jpg', edges)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 12, None, 15, 150)
        xis = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if (x1 == x2) or (abs(x1 - x2) <= 4) or (abs(x2 - x1) <= 4):
                print('x1: ', x1, ', y1: ', y1, ', x2: ', x2, ', y2: ', y2)
                cv2.line(crop_img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                xis.append(x1)

        maior = xis[0]
        menor = xis[0]

        for i in xis:
            if i > maior:
                maior = i

        for i in xis:
            if i < menor:
                menor = i

        subtracao = maior - menor
        print('subtracao: ', subtracao)
        area = subtracao * subtracao
        return area

    def processaImagem(self, caminho, imagemCarregada, threshValue1, threshValue2):
        im1 = 'Acetato 50.JPG'
        im2 = 'Acetato 100.JPG'
        im3 = 'Butanol 50.JPG'
        im4 = "Controle 1.JPG"
        im5 = "imagem5.jpg"
        im6 = "Diabetico 10mg-Kg/4.JPG"

        imagem = []
        if caminho != "":
            imagem = cv2.imread(caminho, 1)
            print(caminho)
        else:
            imagem = imagemCarregada

        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        if caminho == "":
            imagem = imutils.resize(imagem, width=666, height=500)
        else:
            imagem = imutils.resize(imagem, height = 500)

        area = self.medeScala(imagem)
        print('area: ', area)
        #imagem = self.adjust_gamma(imagem, 1.5)
        imagem = cv2.pyrMeanShiftFiltering(imagem, 15, 20)

        imgray = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
        #imgray = self.adjust_gamma(imgray, gamma=1.5)

        r, g, b = cv2.split(imagem)
        h,s,v = cv2.split(imgray)
        #cv2.imshow('gray', cv2.equalizeHist(g))


        invert1 = cv2.bitwise_not(h)
        ret, thresh1 = cv2.threshold(cv2.equalizeHist(g), threshValue1, 255, cv2.THRESH_BINARY)####240############################
        #ret, thresh1 = cv2.threshold(invert1, 220, 255, cv2.THRESH_BINARY)
        #cv2.imwrite('dd1.jpg', thresh1)
        cv2.imshow("dd1",  thresh1)
        height, width = imagem.shape[:2]

        if caminho == "":
            copy_output = np.zeros((height, width, 3), np.uint8)
        else:
            copy_output = np.zeros((500, 666, 3), np.uint8)
        print('copy: ',copy_output.shape)
        np.copyto(copy_output, imagem, where=thresh1[:,:,np.newaxis].astype(bool))
        sub = imagem - copy_output
        sub1 = sub
        sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
        eq = cv2.equalizeHist(sub)
        filter = cv2.bilateralFilter(eq, 15, 25, 25)
        filter = cv2.cvtColor(filter, cv2.COLOR_GRAY2BGR)
        #cv2.imwrite('dd.jpg', filter)
        cv2.imshow("dd", filter)

        #deixar só a area da ilhota separada, para depois cortar a area
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,2))
        erode = cv2.erode(filter, kernel2, iterations=2)
        dilat = cv2.dilate(erode, kernel2, iterations=1)
        ret, thresh1 = cv2.threshold(dilat, threshValue2, 255, cv2.THRESH_BINARY) ##############170####################185-230
        cv2.imwrite('shift.jpg', dilat)
        cv2.imshow("shift1", dilat)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
        erode = cv2.erode(thresh1, kernel2, iterations=6)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dilat = cv2.dilate(erode, kernel2, iterations=8)

        #pegar o contorno dessa area e depois expandi-lo
        plot_image = np.concatenate((dilat, thresh1), axis=1)
        cv2.imwrite('dilat.jpg', dilat)
        cv2.imshow("im", plot_image)
        dilat = cv2.cvtColor(dilat, cv2.COLOR_BGR2GRAY)
        im2, contours, hierarchy = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contorno_maior = 0
        cont = 0
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) > contorno_maior:
                contorno_maior = cv2.contourArea(contours[i])
                cont = i

        M = cv2.moments(contours[cont])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print('cX: ', cX, ' cY: ', cY)

        for i in range(0, len(contours[cont])):
            contours[cont][i][0][0] -= cX
            contours[cont][i][0][1] -= cY

            contours[cont][i][0][0] += (contours[cont][i][0][0] * 0.6)
            contours[cont][i][0][1] += (contours[cont][i][0][1] * 0.6)

            contours[cont][i][0][0] += cX
            contours[cont][i][0][1] += cY
            #print(contours[cont][i][0][0], '  ', contours[cont][i][0][1])



        #com o maior contorno encontrado, cortar sua regiao e tentar eliminar bordas fora da ilhota
        mask = np.zeros(imagem.shape[:2],np.uint8)
        cv2.drawContours(mask, contours, cont, 255, -1)

        dst = cv2.bitwise_and(imagem, sub1, mask=mask)
        #dst = cv2.bitwise_and(imagem, imagem, mask=mask)
        imgray = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(imgray)

        filter = cv2.bilateralFilter(s, 5, 70, 70)
        eq = cv2.equalizeHist(filter)
        invert1 = cv2.bitwise_not(eq)

        invert2 = cv2.cvtColor(invert1, cv2.COLOR_GRAY2BGR, 1)
        shift = cv2.pyrMeanShiftFiltering(invert2, 21, 61)


        #cv2.imshow("cut", dst)

        height, width = dst.shape[:2]
        ret, thresh1 = cv2.threshold(shift, 125, 255, cv2.THRESH_BINARY)
        if caminho == "":
            copy_output = np.zeros((height, width, 3), np.uint8)
        else:
            copy_output = np.zeros((500, 666, 3), np.uint8)

        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        erode = cv2.erode(thresh1, kernel2, iterations=6)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dilate = cv2.dilate(erode, kernel2, iterations=7)
        invert1 = cv2.bitwise_not(dilate)

        cv2.imshow("fdf", invert1)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dilate = cv2.dilate(invert1, kernel2, iterations=2)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        erode = cv2.erode(dilate, kernel2, iterations=1)



        np.copyto(copy_output, dst, where=erode[:,:].astype(bool))
        sub = dst - copy_output

        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dilate = cv2.dilate(sub, kernel2, iterations=5)
        dilate = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY, 1)
        im2, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contorno_maior = 0
        cv2.imwrite('dddCorte.jpg', dilate)
        cv2.imshow("ddd", dilate)
        cont = 0
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) > contorno_maior:
                contorno_maior = cv2.contourArea(contours[i])
                cont = i


        cv2.drawContours(imagem, [contours[cont]], -1, (0, 255, 0), 2)
        #cv2.circle(dilate, (cX, cY), 7, (255, 255, 255), -1)
        '''plot_image = np.concatenate((dst, dilate), axis=1)
        cv2.imshow("plot", plot_image)'''

        if caminho == '':
            imagem = imutils.resize(imagem, height=500)
        adjusted = self.adjust_gamma(imagem, gamma=0.6)


        plot_image = np.concatenate((imagem, adjusted), axis=1)
        #cv2.imwrite("C:/Users/Moacir/Desktop/results/28.jpg", imagem)
        cv2.imwrite('contornado.jpg', imagem)
        cv2.imshow('final', plot_image)
        print(cont)
        if self.contador < 1:
            mask = np.zeros(imagem.shape[:2], np.uint8)
            hull = []
            hull = cv2.convexHull(contours[cont], False)
            #cv2.drawContours(imagem, [hull], -1, (0, 255, 0), 4, 8)
            cv2.drawContours(mask, [hull], -1, 255, -1)
            orig = cv2.imread(caminho, 1)
            #orig = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
            orig = imutils.resize(orig, height=500)
            pts = np.array(hull)
            rect = cv2.boundingRect(pts)
            x, y, w, h = rect
            croped = orig[y:y + h, x:x + w].copy()
            pts = pts - pts.min(axis=0)
            mask = np.zeros(croped.shape[:2], np.uint8)
            cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

            dst = cv2.bitwise_and(croped, croped, mask=mask)
            dst = imutils.resize(dst, width=666, height=500)
            self.contador = 1
            cv2.imshow('hull', dst)
            u = utils.Segment()
            #image = u.processaImagem(dst)
            #cv2.imshow('kmeans', image)
            #cv2.imwrite('hulls/23.jpg', dst)
            #u.segundoProcesso(dst)
            self.contador = 1
            #imagem = self.processaImagem('', dst)
            return area, dst
        elif caminho == '':
            return area, imagem
        else:
            return area, []
#cv2.waitKey(0)