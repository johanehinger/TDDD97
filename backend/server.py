from flask import Flask, request
import database_helper
import math
import random

app = Flask(__name__)

def generateToken():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 36):
        token += letters[math.floor(random.random() * len(letters))]
    return token
    

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# To start the database 
@app.cli.command('initDatabase')
def init_database():
    print("Init DB")
    database_helper.init_db(app)

@app.route("/sign_in", methods=['POST'])
def sign_in():
    email = request.headers.get("email")
    password = request.headers.get("password")
    token = generateToken()
    return {"success": True, "message": "Successfully signed in.", "data": token }

@app.route("/sign_up", methods=["POST"])
def sign_up():
    firstName = request.headers.get("firstname")
    familyName = request.headers.get("familyname")
    gender = request.headers.get("gender")
    city = request.headers.get("city")
    country = request.headers.get("country")
    email = request.headers.get("email")
    password = request.headers.get("password")
    print(firstName)
    print(not (firstName and familyName and gender and city and country))
    print(not ('@' in email))
    
    # Assert that the user doesn't exist.
    if (database_helper.query_db("select * from users WHERE email=?", [email], one=True) != None):
        return {"success": False, "message": "User already exists."}

    # Data must be valid
    if (not (firstName and familyName and gender and city and country) or (len(password)>=5) or not ('@' in email)):
        return {"success": False, "message": "Form data missing or incorrect type."};

    database_helper.query_db("INSERT INTO users(email, city, country, familyname, firstname, gender, password) VALUES(?, ?, ?, ?, ?, ?, ?)", [email, city, country, familyName, firstName, gender, password])
    return {"success": True, "message": "Successfully created a new user."};

@app.route("/print", methods=['GET'])
def test():
    for user in database_helper.query_db("select * from users"):
        print(user)

    return {"success": True, "message": "Print done"}


    