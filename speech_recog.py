# Code by Lilie Boizumault, for QI Informatique, France
# 2020

# files needed :
# ardSerial.py written by Rongzhong Li, Petoi

# many thanks to David Amos for his great tutorial on Speech Recognition
# https://realpython.com/python-speech-recognition/#installing-speechrecognition


#####################################################################

# Controlling Nybble with your voice
# Controler Nybble avec ta voix

#####################################################################


# FIRST STEP : FIND YOUR MICROPHONE
# Uncomment this part, comment the rest

# PREMIERE ETAPE : SELECTIONNER LE BON MICRO
# Decommenter cette partie et commenter le reste


# import speech_recognition as sr

# r = sr.Recognizer()

## utilisation du micro

# affichage de la liste des micro
#print(sr.Microphone.list_microphone_names()) # look for your micro in the list (get the index)
# chercher l'indice du micro voulu


#####################################################################

# SECOND STEP : TEST YOUR MICROPHONE
# Uncomment this part, comment the rest

# DEUXIEME ETAPE : TESTER LE MICRO
# Decommenter cette partie et commenter le reste


# import speech_recognition as sr

# r = sr.Recognizer()
# mic = sr.Microphone(device_index=0)

# with mic as source : 
    # r.adjust_for_ambient_noise(source)
    # audio = r.listen(source)
# print(r.recognize_google(audio, language='fr-FR'))


#####################################################################
# THIRD STEP : SPEECH RECOGNITION AND NYBBLE
# Uncomment this part, comment the rest

# TROISIEME ETAPE : NYBBLE ET LA RECONNAISSANCE VOCALE
# Decommenter cette partie et commenter le reste


## Script de reconnaissance vocale 

#!/usr/bin/python
from ardSerial import * #importer le fichier pour communiquer avec Nybble

import speech_recognition as sr #importer la bibliothèque SpeechRecognition 

# Création des objets Microphone et Recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=0)

# function to translate the "speech" order to "written" order
def recognize_speech(recognizer, microphone) : # fonction qui traduit l'ordre vocal
    # en ordre écrit 
    with microphone as source : # listen to the speech
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try: 
        order = recognizer.recognize_google(audio, language='fr-FR')
    except sr.RequestError: # API unreachable
        # si l'API ne répond pas ou n'est pas joignable 
        order = "error1"
        print("API unavailable")
    except sr.UnknownValueError: # unknown speech
        # le mot n'a pas pu être identifié
        order = "error2"
        print("Unable to recognize speech")
    
    return order 

# this function translate the "written" order in an order for Nybble
# WARNING : FOR ENGLISH USERS --> NEED TO CHANGE THE DETECTED WORDS AND THE LANGUAGE DETECTED IN RECOGNIZE_GOOGLE

def translate_order(order) : #fonction qui traduit l'ordre écrit en ordre pour
# Nybble
    order = order.lower() # on s'assure que le texte est en minuscules 
    if order == "marche" :
        order_nybble = 'kwk'
    elif order == "debout" :
        order_nybble = 'kbalance'
    elif order == "assis" :
        order_nybble = 'ksit'
    elif order == "bonjour" :
        order_nybble = 'whi_Nybble'
    elif order =="stop" :
        order_nybble = 'kbalance'
    elif order =="repos" :
        order_nybble = 'd'
    else : # si l'ordre n'est pas un mot que l'on a code --> ne rien faire
        print(order)
        order_nybble = ' ' # if the order is none of these orders : don't do anything
    return order_nybble 


while(True) : 
    last_task = []
    task = []

    order = recognize_speech(recognizer, microphone)
    order_nybble = translate_order(order)

    if not(order_nybble == ' ') : # si on a reçu un ordre compatible avec Nybble
        task = [order_nybble, 0]   # task to be sended to Nybble

    if not(task == last_task) : # si on n'est pas deja en train de faire cette tache
        # if the order is not the current task
        last_task = task
        wrapper(task)
        print(task)
        if (task == ['d', 0]) : break # si on dit "repos" : fin du script
        # if the order is "rest" --> end of script



