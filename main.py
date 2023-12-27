import os
import winsound
import cv2
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("smart-att-a6ef4-firebase-adminsdk-f43xk-c6c937856d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://smart-att-a6ef4-default-rtdb.firebaseio.com/",
    'storageBucket': "smart-att-a6ef4.appspot.com"
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)
height = 450
width = 760
cap.set(3, width)
cap.set(4, height)

imgBackground = cv2.imread('temps/bg.png')

# importing the overlaying images
folderTempsPath = 'temps/overlay'
modePathList = os.listdir(folderTempsPath)
imgOverlayList = []

for path in modePathList:
    imgOverlayList.append(cv2.imread(os.path.join(folderTempsPath, path)))

# importing Encoding files
print("Loading Encode files...")
file = open('EncodeFile.p', 'rb')
encodeNames = pickle.load(file)
encodeListKnown, studentIds = encodeNames
print("Encode file loaded")

modeType = 0
counter = 0
id = -1
studentInfo = None
imgStudent = []

while True:
    success, img = cap.read()

    if not success:
        break
    profile = cv2.resize(img, (0,0), None, 0.25, 0.25)
    profile = cv2.cvtColor(profile, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(profile)
    encodeCurrentFrame = face_recognition.face_encodings(profile, faceCurrentFrame)

    img = cv2.resize(img, (width, height))
    imgOverlay = imgBackground.copy()  # Create a copy of the background image to draw the bounding boxes

    # placing the webcam
    imgOverlay[185:185 + height, 55:55 + width] = img

    # placing the right indicating images
    imgOverlay[5:5 + 697, 890:890 + 353] = cv2.resize(imgOverlayList[modeType], (353, 697))

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            winsound.Beep(1000, 100)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 5 + x1, 85 + y1, x2 - x1, y2 - y1
            imgOverlay = cvzone.cornerRect(imgOverlay, bbox, rt = 0)
            id = studentIds[matchIndex]
            # print(id)

            if counter == 0:
                counter = 1
                modeType = 1
    if counter != 0:
        if counter == 1:
            #get the data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            #get the image from the db
            blob = bucket.get_blob(f'images/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        cv2.putText(imgOverlay, str(studentInfo['id']), (1010, 385),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 1)
        cv2.putText(imgOverlay, str(studentInfo['name']), (1010, 445),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)

        cv2.putText(imgOverlay, str(studentInfo['class']), (1010, 505),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
        cv2.putText(imgOverlay, str(studentInfo['year']), (1010, 565),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
        cv2.putText(imgOverlay, str(studentInfo['total_att']), (1155, 655),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0,155,23), 1)

        imgOverlay[128:128 + 167, 999:999 + 130] = imgStudent


        counter += 1

    cv2.imshow("Face Attendance", imgOverlay)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit the application
        break

cap.release()
cv2.destroyAllWindows()
