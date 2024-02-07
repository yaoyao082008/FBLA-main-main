# Database Utilities

# modules needed to use file
import firebase_admin
from firebase_admin import firestore, credentials

# Application Default credentials are automatically created.
creds = credentials.Certificate("firebase_creds.json")
app = firebase_admin.initialize_app(creds)
db = firestore.client()

# update user in database
def update_user(email):
    ref = db.collection("users").document(email)
    if not get_user(email): # if user does not exist
        data = {"email": email, "gpa": {}, "classes": []}
    else:
        data = {"email": email}
    try: # try to update data
        ref.update(data)
    except:
        #create data 
        ref.set(data)

# get user from database
def get_user(email):
    ref = db.collection("users").stream()
    for u in ref:
        u = u.to_dict()
        if u["email"] == email:
            return u # return user if exists

# update users classes in database
def update_classes(email, classes):
    ref = db.collection("users").document(email)
    data = {"classes": classes} # set classes
    try:
        ref.update(data)
    except:
        ref.set(data)

# get classes from database
def get_classes(email):
    ref = db.collection("users").stream()
    for usr in ref:
        usr = usr.to_dict()
        if usr["email"] == email:
            return usr["classes"] # if the user email matches, return classes

# update gpa in database
def update_gpa(email, w_gpa, uw_gpa):
    ref = db.collection("users").document(email)
    data = {"gpa": {"w_gpa": w_gpa, "uw_gpa": uw_gpa}} # set gpa data
    try:
        ref.update(data)
    except:
        ref.set(data)

# get gpa from database
def get_gpa(email):
    ref = db.collection("users").stream()
    for usr in ref:
        usr = usr.to_dict()
        if usr["email"] == email:
            return usr["gpa"] # if user email matches, return gpas