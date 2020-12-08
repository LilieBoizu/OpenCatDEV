# Code by Lilie Boizumault, for QI Informatique, France
# 2020

# file needed :
# ardSerial.py written by Rongzhong Li, Petoi

# many thanks to Murtaza Hassan for his amazing tutorial on opencv :
# https://www.youtube.com/watch?v=WQeoO7MI0Bs

#####################################################################

# Controlling Nybble with colours
# Controler Nybble avec des couleurs

#####################################################################

#!/usr/bin/python3
from ardSerial import *
import cv2 as cv
import picamera
import numpy


#####################################################################

# First step : find HSV values for your colors --> uncomment this part / comment the rest
# Premiere etape : trouver les valeurs HSV de vos couleurs
# --> decommenter cette partie / commenter le reste

#####################################################################

# def empty(a):
# pass

# cv.namedWindow("HSV")
# cv.resizeWindow("HSV",640,240)
# cv.createTrackbar("HUE Min","HSV",0,179,empty)
# cv.createTrackbar("SAT Min","HSV",0,255,empty)
# cv.createTrackbar("VALUE Min","HSV",0,255,empty)
# cv.createTrackbar("HUE Max","HSV",179,179,empty)
# cv.createTrackbar("SAT Max","HSV",255,255,empty)
# cv.createTrackbar("VALUE Max","HSV",255,255,empty)


# while True :

# ## Initialisation : on définit la caméra utilisée
# with picamera.PiCamera() as camera : # appel de la fonction crée pour une PiCamera
# camera.resolution = (640, 480) # réglage de la taille de l'image
# image = numpy.empty((480*640*3,), dtype = numpy.uint8)
# camera.capture(image, 'bgr')
# image = image.reshape((480, 640, 3))

# imgHsv = cv.cvtColor(image,cv.COLOR_BGR2HSV)

# h_min = cv.getTrackbarPos("HUE Min","HSV")
# h_max = cv.getTrackbarPos("HUE Max", "HSV")
# s_min = cv.getTrackbarPos("SAT Min", "HSV")
# s_max = cv.getTrackbarPos("SAT Max", "HSV")
# v_min = cv.getTrackbarPos("VALUE Min", "HSV")
# v_max = cv.getTrackbarPos("VALUE Max", "HSV")

# lower = numpy.array([h_min,s_min,v_min])
# upper = numpy.array([h_max,s_max,v_max])
# mask = cv.inRange(imgHsv,lower,upper)
# result = cv.bitwise_and(image,image, mask = mask)

# mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)


# cv.imshow('Mask', mask)
# cv.imshow('Result', result)


# k = cv.waitKey(30) & 0xff
# if k == 27 :
# break

#####################################################################

# Second step : testing on Nybble --> comment the part above and uncomment
# the following part
# Deuxieme etape : tester sur Nybble --> commenter la partie ci-dessus et
# d2commenter la partie suivante

#####################################################################



# Definition des competences de Nybble a utiliser
# Nybble skills to be used in this script
walk = ['kwk',0]
rest = ['d',2]
stand = ['kbalance',2]
sit = ['ksit',2]

# couleurs en HSV : [hmin, smin, vmin, hmax, smax, vmax] (cf premiere etape)
# --> ADAPTER SELON VOS COULEURS <--

# colours (HSV) :  [hmin, smin, vmin, hmax, smax, vmax] (see first step)
# --> VALUES TO BE UPDATED WITH YOUR OWN COLOR VALUES  <--
colors = [[75, 0, 96, 148, 146, 218], #vert
          [92, 111, 131, 146, 255, 255]] #bleu

colors_names = ['green','blue','none']

# cette fonction renvoie le nom de la couleurs detectee : si 2 ou plus --> renvoie 'none'
# this function returns the name of the color detected : if 2 or more colors --> returns none
def findColor(img,colors, colors_names):
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    color_id=[]
    color_name=''
    for color in colors:
        lower = numpy.array(color[0:3])
        upper = numpy.array(color[3:6])
        mask = cv.inRange(imgHSV,lower,upper)
        is_color = IsColor(mask)
        if is_color :
            color_id.append(count)
        count +=1
    if len(color_id)==1 :
        color_name = colors_names[color_id[0]]
    else :
        color_name = colors_names[len(colors_names)-1]
    return color_name

# this functions looks for colors
# cette fonction recherche les couleurs
def IsColor(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    is_color = False
    for cnt in contours:
        area = cv.contourArea(cnt)
        
        if area>40000: # la surface de la couleur detectee doit etre suffisamment grande (filtrage des autres couleurs du paysage)
            is_color = True
    return  is_color



start = False # indicate whether Nybble is walking

# init : Nybble stands
# init : Nybble se met debout
wrapper(stand)

while True:

    ## Capture video avec la camera
    ## Video capture with Raspi camera
    with picamera.PiCamera() as camera : # appel de la fonction crée pour une PiCamera
        camera.resolution = (640, 480) # réglage de la taille de l'image
        image = numpy.empty((480*640*3,), dtype = numpy.uint8) # conversion de l'image pour opencv
        camera.capture(image, 'bgr')
        image = image.reshape((480, 640, 3)) # opencv image

    color_name = findColor(image, colors, colors_names) # find color / trouver la couleur
    print("color : ", color_name)

    #cv.imshow('Original', image)

    ## Definition des actions a effectuer selon la couleur detectee
    ## Definition of  the orders given to Nybble according to the color detected
    # feel free to add many colors and skills
    if color_name=='green' and not(start): # si Nybble voit du vert, et qu'il n'est pas deja en train de marcher
        start = True
        print('walk')
        wrapper(walk)
    if color_name == 'blue' and start: # si Nybble voit du bleu et qu'il est en train de marcher
        start = False
        print('rest')
        wrapper(stand)
        wrapper(sit)

    # k = cv.waitKey(30) & 0xff
    # if k == 27 :
    #     break
