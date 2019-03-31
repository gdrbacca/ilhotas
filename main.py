import cv2
import numpy as np
import imutils


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

im1 = 'Acetato 50.JPG'
im2 = 'Acetato 100.JPG'
im3 = 'Butanol 50.JPG'
im4 = "Controle 1.JPG"
im5 = "imagem5.jpg"
im6 = "Controle 5mg-Kg\\3.JPG"

imagem = cv2.imread(im6, 1)
imagem = imutils.resize(imagem, height = 500)
imagem = adjust_gamma(imagem, gamma=1.5)
imagem = cv2.pyrMeanShiftFiltering(imagem, 15, 18)

imgray = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
imgray = adjust_gamma(imgray, gamma=1.5)

r, g, b = cv2.split(imagem)
h,s,v = cv2.split(imgray)
eqg = cv2.equalizeHist(r)

invert1 = cv2.bitwise_not(h)
ret, thresh1 = cv2.threshold(cv2.equalizeHist(g), 240, 255, cv2.THRESH_BINARY)###################################
#ret, thresh1 = cv2.threshold(invert1, 215, 255, cv2.THRESH_BINARY)
cv2.imshow("dd1",  thresh1)
copy_output = np.zeros((500, 666, 3), np.uint8)
np.copyto(copy_output, imagem, where=thresh1[:,:,np.newaxis].astype(bool))
sub = imagem - copy_output
sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
eq = cv2.equalizeHist(sub)
filter = cv2.bilateralFilter(eq, 15, 25, 25)
filter = cv2.cvtColor(filter, cv2.COLOR_GRAY2BGR)
cv2.imshow("dd", filter)

#deixar só a area da ilhota separada, para depois cortar a area
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,2))
erode = cv2.erode(filter, kernel2, iterations=2)
dilat = cv2.dilate(erode, kernel2, iterations=1)
ret, thresh1 = cv2.threshold(dilat, 186, 255, cv2.THRESH_BINARY) #####################################215, 225
cv2.imshow("shift1", dilat)
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
erode = cv2.erode(thresh1, kernel2, iterations=6)
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
dilat = cv2.dilate(erode, kernel2, iterations=8)

#pegar o contorno dessa area e depois expandi-lo
plot_image = np.concatenate((dilat, thresh1), axis=1)
cv2.imshow("im", plot_image)
dilat = cv2.cvtColor(dilat, cv2.COLOR_BGR2GRAY)
im2, contours, hierarchy = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contorno_maior = 0;
cont = 0;
for i in range(0, len(contours)):
    print(i,' : ',len(contours[i]))
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
    print(contours[cont][i][0][0], '  ', contours[cont][i][0][1])



#com o maior contorno encontrado, cortar sua regiao e tentar eliminar bordas fora da ilhota
mask = np.zeros(imagem.shape[:2],np.uint8)
cv2.drawContours(mask, contours, cont, 255, -1)

dst = cv2.bitwise_and(imagem, imagem, mask=mask)
imgray = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(imgray)

filter = cv2.bilateralFilter(s, 5, 70, 70)
eq = cv2.equalizeHist(filter)
invert1 = cv2.bitwise_not(eq)

invert2 = cv2.cvtColor(invert1, cv2.COLOR_GRAY2BGR, 1)
shift = cv2.pyrMeanShiftFiltering(invert2, 21, 61)


cv2.imshow("cut", dst)


ret, thresh1 = cv2.threshold(shift, 120, 255, cv2.THRESH_BINARY)
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
dilate = cv2.dilate(sub, kernel2, iterations=3)
dilate = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY, 1)
im2, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contorno_maior = 0;
cv2.imshow("ddd", dilate)
cont = 0;
for i in range(0, len(contours)):
    print(i,' : ',len(contours[i]))
    if cv2.contourArea(contours[i]) > contorno_maior:
        contorno_maior = cv2.contourArea(contours[i])
        cont = i


cv2.drawContours(imagem, [contours[cont]], -1, (255, 255, 255), 1)
#cv2.circle(dilate, (cX, cY), 7, (255, 255, 255), -1)
'''plot_image = np.concatenate((dst, dilate), axis=1)
cv2.imshow("plot", plot_image)'''
adjusted = adjust_gamma(imagem, gamma=0.6)
plot_image = np.concatenate((imagem, adjusted), axis=1)
#cv2.imwrite("im4.jpg", imagem)
cv2.imshow('final', plot_image)
print(cont)

cv2.waitKey(0)