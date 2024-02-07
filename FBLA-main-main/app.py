
# Library Requirements
from flask import Flask, render_template, request, session, redirect, jsonify
import json, datetime
from db import *
from functools import wraps
from utils import num_gpa_calc, total_num_gpa_calc

# wrapper function (checks if user is logged in)
def logged_in_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if session.get("user") is None:
            return redirect('/')
        return func(*args, **kwargs)

    return decorator

# initialization 
app = Flask(__name__)
app.secret_key = "syIyJRgEcuUQ8XI9iG-fA3slxHTBMmk"
app.permanent_session_lifetime = datetime.timedelta(days=31)


# home page
@app.route('/')
def home():
    return render_template("index.html", logged_in=session.get("user"))


# main calculator page
@app.route('/calculator')
@logged_in_required
def calculator():
    print(get_classes(session.get("user")["email"]))
    # loads "calculator.html" file, and passes in required variables
    return render_template(
        "calculator.html",
        logged_in=True,
        classes=get_classes(session.get("user")["email"]),
        w_gpa=session.get("w_gpa"),
        uw_gpa=session.get("uw_gpa")
    )


# web hook for updating classes/gpa
@app.route('/update_calc', methods=["POST"])
@logged_in_required
def update_calc():
    # get all class names, types, and numerical grades
    names = request.form.getlist("names[]")
    types = request.form.getlist("types[]")
    num_grades = request.form.getlist("num_grades[]")

    classes = {} # dictionary to store classes

    # data formating
    for i in range(len(names)):
        num_grades[i] = int(num_grades[i])
        classes[names[i]] = [types[i], num_grades[i], num_gpa_calc(types[i], num_grades[i], False), num_gpa_calc(types[i], num_grades[i], True)]
        
    update_classes(session.get("user")['email'], classes) # updates classes in database

    # gpa calculation
    uw_gpa = total_num_gpa_calc([c[2] for c in classes.values()])
    w_gpa = total_num_gpa_calc([c[3] for c in classes.values()])

    # gpa storage in the browser session
    session["uw_gpa"] = uw_gpa 
    session["w_gpa"] = w_gpa
    session.modified = True
    
    update_gpa(session.get("user")["email"], w_gpa, uw_gpa)# update gpa in database

    return jsonify({"":""}) # tells server success

# login link
@app.route('/login', methods=["POST"])
def login():
    user = json.loads(request.form.get("creds")) # gets user login info
    update_user(user["email"]) # updates user email in database
    session["user"] = user # stores user in browswer session
    gpas = get_gpa(user["email"]) # gets user gpa

    # store gpa if they exist
    if gpas:
        session["w_gpa"] = gpas["w_gpa"]
        session["uw_gpa"] = gpas["uw_gpa"]
        session.modified = True

    session.permanent = True

    return ""

# logout link
@app.route('/logout', methods=["POST"])
def logout():
    session.clear() # clear browser session
    session.modified = True
    return ""

# run app
if __name__ == "__main__":
    app.run(host="localhost", debug=True)