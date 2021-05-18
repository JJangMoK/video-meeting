import cv2
import numpy as np
import face_recognition
import os


class FaceRec:
    def __init__(self, path):
        images = []
        self.avgfd = []
        self.classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
            print(self.classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        self.encodeListKnown = findEncodings(images)
        print('Encoding Complete')

    def recognize(self, img):
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.\
                compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.\
                face_distance(self.encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                avgfaceDis = sum(faceDis)/5
                self.avgfd.append(1 - avgfaceDis)

        return img

    def clean_list(self):
        self.avgfd = []

    def get_result(self):
        return self.avgfd.copy()
