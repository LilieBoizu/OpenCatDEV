# Code by Lilie Boizumault, for QI Informatique, France
# 2020

# files needed :
# ardSerial.py written by Rongzhong Li, Petoi
# haarcascade_frontalface_default.xml by Murtaza Hassan : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours (ressources)

# many thanks to Murtaza Hassan for his amazing tutorial on opencv :
# https://www.youtube.com/watch?v=WQeoO7MI0Bs


#!/usr/bin/python3
from ardSerial import *
import cv2 as cv
import picamera
import numpy

#####################################################################

# Nybble says hi when he sees a human face
# Nybble dit Bonjour quand il voit un visage humain

#####################################################################

# Init pour la detection de visage
# cascade file for face detection

# --> Don't forget to change the path of the .xml file  <--
# --> Ne pas oublier de changer le chemin du fichier .xml <--
faceCascade = cv.CascadeClassifier("/home/pi/Petoi/OpenCv/haarcascade_frontalface_default.xml")  # fichier Cascade

# this function returns true if a human face is detected
# cette fonction renvoie vrai si un visage est detecte
def detect_faces(image):

    imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # conversion en image en niveaux de gris
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)  # detection visages
    
    #for (x,y,w,h) in faces: # on parcourt tous les visages
        #cv.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2) # on trace un rectangle autour des visages
        
    if len(faces)>0 :
        return True
    else :
        return False


task_init = ['ksit',3]
task_detect = ['whiNybble',10]
rest = ['d',5]

# Init
wrapper(task_init)


while True :

    ## Capture video avec la camera
    ## Video capture with Raspi camera
    with picamera.PiCamera() as camera : # appel de la fonction crée pour une PiCamera
        camera.resolution = (640, 480) # réglage de la taille de l'image
        image = numpy.empty((480*640*3,), dtype = numpy.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((480, 640, 3))
    
    face = detect_faces(image)
    print("Face detected ? ", face)
    
    
    #cv.imshow('image', image)
    #k = cv.waitKey(30) & 0xff
    #if k == 27 :
        #break
        
    if face : break # si on voit un visage : on sort de la boucle
    

# when a face is detected
# quand un visage est detecte
wrapper(task_detect)
wrapper(rest)



