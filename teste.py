import utils
import cv2
import numpy as np
import imutils
from scipy import signal
from skimage.future import graph
from skimage import data, io, segmentation, color
from matplotlib import pyplot as plt

'''def gaussian_kernel(k, s=0.5):
    # generate a (2k+1)x(2k+1) gaussian kernel with mean=0 and sigma = s
    probs = [np.exp(-z * z / (2 * s * s)) / np.sqrt(2 * np.pi * s * s) for z in range(-k, k + 1)]
    return np.outer(probs, probs)


def create_graph(imfile, k=1., sigma=0.8, sz=1):
    # create the pixel graph with edge weights as dissimilarities
    rgb = mpimg.imread(imfile)[:, :, :3]
    gauss_kernel = gaussian_kernel(sz, sigma)
    for i in range(3):
        rgb[:, :, i] = signal.convolve2d(rgb[:, :, i], gauss_kernel, boundary='symm', mode='same')
    yuv = rgb2yiq(rgb)
    (w, h) = yuv.shape[:2]
    edges = {}
    for i in range(yuv.shape[0]):
        for j in range(yuv.shape[1]):
            # compute edge weight for nbd pixel nodes for the node i,j
            for i1 in range(i - 1, i + 2):
                for j1 in range(j - 1, j + 2):
                    if i1 == i and j1 == j: continue

                    if i1 >= 0 and i1 == 0 and j1 < h:
                        wt = np.abs(yuv[i, j, 0] - yuv[i1, j1, 0])
                        
                        n1, n2 = ij2id(i, j, w, h), np.ij2id(i1, j1, w, h)
                        edges[n1, n2] = edges[n2, n1] = wt
    return edges'''



img = cv2.imread('imagensMarcadas/11.jpg')
image = imutils.resize(img, width=666, height=500)
h, w = image.shape[:2]
cv2.imshow('original', image)
cv2.imwrite('fff.jpg', image)
print(h, ' ', w)
#crop_img = img[y:y+h, x:x+w]
crop_img = image[h-50:h, w-80:w]
crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY, 1)
ret, thresh = cv2.threshold(crop_img, 60, 255, cv2.THRESH_BINARY)
cv2.imshow('rr', thresh)
edges = cv2.Canny(thresh, 200, 500, None, 3)
cv2.imshow("canny", edges)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 12, None, 15, 150)
xis = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    if (x1 == x2) or (abs(x1 - x2) <= 4) or (abs(x2 - x1) <= 4):
        print('x1: ',x1,', y1: ', y1,', x2: ', x2,', y2: ',y2)
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
area = subtracao * subtracao
print('menor: ',menor)
print('maior: ',maior)
print('area: ',area)
cv2.imshow("cropped", crop_img)

cv2.waitKey(0)
