import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("smart-att-a6ef4-firebase-adminsdk-f43xk-c6c937856d.json")
firebase_admin.initialize_app(cred, {
        'databaseURL': "https://smart-att-a6ef4-default-rtdb.firebaseio.com/"
    })

ref = db.reference('Students')

data = {
        "001": {
            "id": 2213213037001,
            "name": "Akash A",
            "class": "MCA",
            "year": "II",
            "total_att": 6
        },
        "011": {
            "id": 2213213037011,
            "name": "Sudharsanan SK",
            "class": "MCA",
            "year": "II",
            "total_att": 7
        },
        "013": {
            "id": 2213213037013,
            "name": "Yuvraj Singh",
            "class": "MCA",
            "year": "II",
            "total_att": 12
        }
    }

for key, value in data.items():
        ref.child(key).set(value)
        print("Data added successfully!")


