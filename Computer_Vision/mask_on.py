# Code by Lilie Boizumault, for QI Informatique, France
# 2020

# files needed :
# ardSerial.py written by Rongzhong Li, Petoi
# haarcascade_frontalface_default.xml by Murtaza Hassan : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours (ressources)
# pre-trained model for mask detection mask_recog_ver2.h5 by Hussain Mujtaba : https://drive.google.com/file/d/16uMH4YwdkA8sdnMlJNE7nv_tBJkX5eNe/view

# many thanks to Hussain Mujtaba for his article Real-Time Face Detection on the Great Learning Blog
# https://www.mygreatlearning.com/blog/real-time-face-detection/#sh2

# many thanks to Murtaza Hassan for his amazing tutorial on opencv :
# https://www.youtube.com/watch?v=WQeoO7MI0Bs

#####################################################################

# Nybble gets angry when you don't wear your mask
# Nybble s'ennerve quand vous ne portez pas votre masque

#####################################################################

#!/usr/bin/python3
from ardSerial import *
import cv2 as cv
import picamera
import numpy

## Détection du masque 

from tensorflow.keras.preprocessing.image import img_to_array #importer les fonctions TensorFlow pour l'application du model masque 
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# Init pour la detection de visage
# cascade file for face detection

# --> Don't forget to change the path of the .xml file  <--
# --> Ne pas oublier de changer le chemin du fichier .xml <--
faceCascade = cv.CascadeClassifier("/home/pi/Petoi/OpenCv/haarcascade_frontalface_default.xml")
model = load_model("mask_recog_ver2.h5") # modèle de detection de masque

# function to detect if there is a face, and if the face wears a mask
# fonction qui indique si un visage est detecte, et si le visage porte un masque
def detect_mask(image):
    face = False
    maskon = False
    imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # conversion en image en niveaux de gris
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)  # detection visages
    faces_list=[] # liste des visages 
    preds=[] # liste des prédictions du détecteur de masque 
    
    for (x,y,w,h) in faces: # on parcourt tous les visages
        face_frame = image[y:y+h,x:x+w] # on étudie le visage détecté 
        face_frame = cv.cvtColor(face_frame, cv.COLOR_BGR2RGB)
        face_frame = cv.resize(face_frame, (224, 224))
        face_frame = img_to_array(face_frame)
        face_frame = numpy.expand_dims(face_frame, axis=0)
        face_frame =  preprocess_input(face_frame)
        
        faces_list.append(face_frame) #ajout du visage à la liste des visages 
        if len(faces_list)>0: #si on a un visage 
            face = True
            preds = model.predict(faces_list) # application du modèle de masque 
        for pred in preds:
            (mask, withoutMask) = pred # probabilité de porter un masque ou non 
            print('masque = ', mask)
            print(' pas masque =' ,withoutMask)
            
            if mask > 0.80 : 
                maskon = True
                #cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2) # on trace un rectangle autour des visages en VERT
            #else : cv.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2) # on trace un rectangle autour des visages en ROUGE
        
        
        
    return face, maskon

# Nybble tasks def
task_init = ['ksit',3]
task_mask = ['whiNybble',10]
task_angry = ['kbuttUp', 5]
warning = ['b70 200',1]
rest = ['d',5]

# Init
wrapper(task_init)


# Previous version : Nybble stops if you wear a mask, and if you don't
## Nybble s'arrete quand il a identifié si il y a un visage ou non 
# count = 0
# sequence = []
# while count < 20 :
    
    # ## Initialisation : on définit la caméra utilisée
    # with picamera.PiCamera() as camera : # appel de la fonction crée pour une PiCamera
        # camera.resolution = (640, 480) # réglage de la taille de l'image
        # image = numpy.empty((480*640*3,), dtype = numpy.uint8)
        # camera.capture(image, 'bgr')
        # image = image.reshape((480, 640, 3))
    
    # #print('appel fonction num', count)
    # face, maskon = detect_mask(image)
    # print(face, ' masque : ', maskon)
    # if face and maskon : sequence = [task_mask]
    # #if sequence == [task_mask]: break
    # if face and not(maskon) : sequence= [task_angry]
    # if sequence == [task_mask] or sequence == [task_angry]: break
	# #if sequence == [task_mask] or sequence= [warning, task_angry]: break
		
    # #cv.imshow('image', image)
    
    # # k = cv.waitKey(30) & 0xff
    # # if k == 27 :
        # # break
        
    
    
    # count +=1 


# for task in sequence : 
	# wrapper(task)
# wrapper(rest)



# current version : Nybble waits until you wear your mask
## Nybble attend qu'on mette le masque 
wait_mask = False 
while True :

    ## Capture video avec la camera
    ## Video capture with Raspi camera
    with picamera.PiCamera() as camera : # appel de la fonction crée pour une PiCamera
        camera.resolution = (640, 480) # réglage de la taille de l'image
        image = numpy.empty((480*640*3,), dtype = numpy.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((480, 640, 3))
    

    face, maskon = detect_mask(image)
    print(face, ' masque : ', maskon)
    if face and maskon : break # si on a un visage et qu'il porte un masque --> on sort de la boucle
    if face and not(maskon) and not(wait_mask): # si on a visage et qu'il ne porte pas de masque --> on attend
        wait_mask = True 
        wrapper(task_angry)
    

# when the face wears a mask
# quand le visage a bien mis son masque
wrapper(task_mask) # Nybble says hi
wrapper(rest)
