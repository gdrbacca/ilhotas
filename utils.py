import cv2
import numpy as np
import imutils
import graph
from skimage import data, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt
import tkfilebrowser


class Segment:
    def __init__(self, segments=2):
        self.segments = segments

    def kmeans(self, image):
        image = cv2.GaussianBlur(image, (7, 7), 0)
        vectorized = image.reshape(-1, 3)
        vectorized = np.float32(vectorized)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 5.0)
        ret, label, center = cv2.kmeans(vectorized, self.segments, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        res = center[label.flatten()]
        segmented_image = res.reshape((image.shape))
        return label.reshape((image.shape[0], image.shape[1])), segmented_image.astype(np.uint8)

    def extractComponent(self, image, label_image, label):
        component = np.zeros(image.shape, np.uint8)
        component[label_image == label] = image[label_image == label]
        return component



    def processaImagem(self, imagem):

        #caminho = tkfilebrowser.askopenfilename()
        image = imagem #cv2.imread(caminho, 1)
        image = imutils.resize(image, height=500)
        filter = cv2.bilateralFilter(image, 15, 25, 25)
        image = cv2.pyrMeanShiftFiltering(image, 18, 22)


        cv2.imshow("sub", image)
        '''if len(sys.argv) == 3:
    
            seg = Segment()
            label, result = seg.kmeans(image)
        else:'''
        seg = Segment(3)
        label, result = seg.kmeans(image)

       # cv2.imshow("orig", image)
        #cv2.imshow("segmented", result)
        #result = seg.extractComponent(image, label, 3)
        #cv2.imshow("extracted", result)
        return result
        #cv2.waitKey(0)

    def segundoProcesso(self, image):
        #newimage = graph.get_segmented_image(1.0, 8, 10.0, 2000, image)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        r,g,b = cv2.split(rgb)
        eq = cv2.equalizeHist(g)
        eq = cv2.bitwise_not(eq)

        seg = Segment(3)
        imagem = []
        label, imagem = seg.kmeans(image)
        cv2.imshow('rgb', imagem)
        #image = np.reshape(imagem, (492, 666))
        segments = segmentation.slic(image, n_segments=500, sigma=2)
        cv2.imshow('slic' ,segmentation.mark_boundaries(image, segments))

    def adjust_gamma(self, image, gamma):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def circularidade(self, contorno):
        perimeter = cv2.arcLength(contorno, True)
        area = cv2.contourArea(contorno)
        if perimeter == 0:
            return False
        circularity = 4 * np.pi * (area / perimeter * perimeter)
        print('Circularidade: ', circularity)
        if 0.8 < circularity < 1.2:
            return True
        else:
            return False

#if __name__ == "__main__":
    def processa2(self, caminho):
        img = cv2.imread('hulls/16.jpg')
        seg = Segment(6)
        img = cv2.pyrMeanShiftFiltering(img, 15, 20)
        img = seg.adjust_gamma(img, 1.2)
        img = imutils.resize(img, height=500)
        height, width = img.shape[:2]

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        r,g,b = cv2.split(rgb)
        ret, thresh1 = cv2.threshold(cv2.equalizeHist(g), 240, 255, cv2.THRESH_BINARY)
        copy_output = np.zeros((height, width, 3), np.uint8)
        np.copyto(copy_output, img, where=thresh1[:, :, np.newaxis].astype(bool))
        sub = img - copy_output


        imagem = []
        label, imagem = seg.kmeans(sub)


        invert2 = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY, 1)
        ret, thresh2 = cv2.threshold(invert2, 153, 255, cv2.THRESH_BINARY)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        erode = cv2.erode(thresh2, kernel2, iterations=6)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilat = cv2.dilate(erode, kernel2, iterations=8)
        cv2.imshow('dilat', dilat)
        im2, contours, hierarchy = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contorno_maior = 0;
        cont = 0;
        for i in range(0, len(contours)):
            print(i, ' : ', len(contours[i]))
            if cv2.contourArea(contours[i]) > contorno_maior:
                contorno_maior = cv2.contourArea(contours[i])
                cont = i

        circular = self.circularidade(contorno_maior)

        cv2.drawContours(img, contours, cont, 255, 1)

        cv2.imshow('g', g)
        cv2.imshow('orig', img)
        cv2.imshow('thresh', thresh2)
        cv2.imshow('gray', invert2)
        cv2.imshow('kmeans', imagem)
        plt.tight_layout()
        return img
        #cv2.waitKey(0)
        ##################testar slic com canal preto e branco

    def processaFinal(self, imagem, valueThresh):
        img = imagem #cv2.imread('hulls/16.jpg')
        seg = Segment(6)
        img = cv2.pyrMeanShiftFiltering(img, 15, 20)
        img = seg.adjust_gamma(img, 1.2)
        img = imutils.resize(img, height=500)
        height, width = img.shape[:2]

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        r,g,b = cv2.split(rgb)
        ret, thresh = cv2.threshold(cv2.equalizeHist(g), 240, 255, cv2.THRESH_BINARY)
        copy_output = np.zeros((height, width, 3), np.uint8)
        np.copyto(copy_output, img, where=thresh[:, :, np.newaxis].astype(bool))
        sub = img - copy_output


        imagem = []
        label, imagem = seg.kmeans(sub)


        invert2 = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY, 1)
        ret, thresh2 = cv2.threshold(invert2, valueThresh, 255, cv2.THRESH_BINARY)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        erode = cv2.erode(thresh2, kernel2, iterations=6)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilat = cv2.dilate(erode, kernel2, iterations=8)
        cv2.imshow('dilat', dilat)
        im2, contours, hierarchy = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contorno_maior = 0;
        cont = 0;
        for i in range(0, len(contours)):
            print(i, ' : ', len(contours[i]))
            if cv2.contourArea(contours[i]) > contorno_maior:
                contorno_maior = cv2.contourArea(contours[i])
                cont = i

        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.drawContours(img, contours, cont, (255, 255, 255), 3)
        img = imutils.resize(img, width=666, height=500)
        cv2.imshow('g', g)
        cv2.imshow('orig', img)
        cv2.imshow('thresh', thresh2)
        cv2.imshow('gray', invert2)
        cv2.imshow('kmeans', imagem)
        plt.tight_layout()
        return contorno_maior, contours, cont, img
        #cv2.waitKey(0)
        ##################testar slic com canal preto e branco