import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("smart-att-a6ef4-firebase-adminsdk-f43xk-c6c937856d.json")
firebase_admin.initialize_app(cred, {
        'databaseURL': "https://smart-att-a6ef4-default-rtdb.firebaseio.com/",
        'storageBucket':"smart-att-a6ef4.appspot.com"
    })

# importing the students images
folderImgsPath = 'images'
pathList = os.listdir(folderImgsPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderImgsPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderImgsPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncoding(imagesList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print('Encoding Started......')
encodeListKnown = findEncoding(imgList)
encodeNames = [encodeListKnown, studentIds]
print(encodeListKnown)
print('Encoding Completed')

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeNames, file)
file.close()
print('File Saved')