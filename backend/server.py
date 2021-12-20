from flask import Flask, request
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

@app.route("/sign_in", methods=['POST'])
def sign_in():
    email = request.headers.get("email")
    password = request.headers.get("password")
    token = generateToken()
    return {"success": True, "message": "Successfully signed in.", "data": token }


    