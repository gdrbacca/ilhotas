import cv2
import numpy as np
import imutils
import graph
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
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


#if __name__ == "__main__":
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

        seg = Segment(4)
        imagem = []
        label, imagem = seg.kmeans(image)
        cv2.imshow('rgb', imagem)
        #image = np.reshape(imagem, (492, 666))
        segments = slic(image, n_segments=500, sigma=2)
        cv2.imshow('slic' ,mark_boundaries(image, segments))


        ##################testar slic com canal preto e branco