import cv2
import numpy as np
import os

RECOGINZER = cv2.face.LBPHFaceRecognizer_create()
PASS_CONF = 50
FACE_CASCADE = cv2.CascadeClassifier(os.getcwd() + "\\cascades\\haarcascade_frontalface_default.xml")


def train(photos, lables):
    RECOGINZER.train(photos, np.array(lables))


def found_face(gary_img):
    faces = FACE_CASCADE.detectMultiScale(gary_img, 1.15, 4)
    return len(faces) > 0


def recognise_faces(photos):
    label, confidence = RECOGINZER.predict(photos)
    print("cc==:"+str(confidence))
    if confidence > 60:
        return -1
    return label
