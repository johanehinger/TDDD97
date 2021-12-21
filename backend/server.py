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
    """
    Authenticates the username by the provided password.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    # Assert that the user does exist and that the password is correct!
    if (not database_helper.query_db("select * from users WHERE email=? AND password=?", [email, password], one=True)):
        return {"success": False, "message": "Wrong username or password."};
    
    token = generateToken()
    database_helper.query_db("INSERT INTO loggedinusers(token, email) VALUES(?, ?)", [token, email])
    return {"success": True, "message": "Successfully signed in.", "data": token }

@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Registers a user in the database.
    """
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
    if (not (firstName and familyName and gender and city and country) or (len(password)<5) or not ('@' in email)):
        return {"success": False, "message": "Form data missing or incorrect type."};

    database_helper.query_db("INSERT INTO users(email, city, country, familyname, firstname, gender, password) VALUES(?, ?, ?, ?, ?, ?, ?)", [email, city, country, familyName, firstName, gender, password])
    return {"success": True, "message": "Successfully created a new user."};


@app.route("/sign_out", methods=["POST"])
def sign_out():
    """
    Signs out a user from the system.
    """
    token = request.headers.get("token")
    if (not database_helper.query_db("select * from loggedinusers WHERE token=?", [token], one=True)):
        return {"success": False, "message": "You are not signed in."}
    
    database_helper.query_db("DELETE FROM loggedinusers WHERE token=?", [token])
    return {"success": True, "message": "Successfully signed out."}


@app.route("/change_password", methods=["POST"])
def change_password():
    """
    Changes the password of the current user to a new one.
    """
    token = request.headers.get("token")
    oldPassword = request.headers.get("oldpassword")
    newPassword = request.headers.get("newpassword")
    email = database_helper.query_db("SELECT email from loggedinusers WHERE token=?", [token], one=True)

    if (not email):
        return {"success": False, "message": "You are not logged in."} 

    if (not database_helper.query_db("select * from users WHERE password=? and email=?", [oldPassword, email[0]], one=True)):
        return {"success": False, "message": "Wrong password."}

    database_helper.query_db("UPDATE users SET password=? WHERE email=?", [newPassword, email[0]])
    return {"success": True, "message": "Password changed."}


@app.route("/get_user_data_by_token", methods=["POST"])
def get_user_data_by_token():
    """
    Retrieves the stored data for the user whom the passed token is issued for. The currently
    signed in user can use this method to retrieve all its own information from the server
    """
    token = request.headers.get("token")
    email = database_helper.query_db("SELECT email from loggedinusers WHERE token=?", [token], one=True)

    if (not email):
        return {"success": False, "message": "You are not signed in."}

    user = database_helper.query_db("SELECT email from users WHERE email=?", [email[0]], one=True)

    if (not user):
        return {"success": False, "message": "No such user."}   

    data = database_helper.query_db("select * from users WHERE email=?", [email[0]], one=True)
    match = {
        "email": data[0],
        "city": data[1],
        "country": data[2],
        "familyname": data[3],
        "firstname": data[4],
        "gender": data[5]
    }

    return {"success": True, "message": "User data retrieved.", "data": match};


@app.route("/get_user_data_by_email", methods=["POST"])
def get_user_data_by_email():
    """
    Retrieves the stored data for the user specified by the passed email address.
    """
    token = request.headers.get("token")
    email = request.headers.get("email")

    if (not database_helper.query_db("SELECT * from loggedinusers WHERE token=?", [token], one=True)):
        return {"success": False, "message": "You are not signed in."}

    user = database_helper.query_db("SELECT * from users WHERE email=?", [email], one=True)
    print(user)
    if (not user):
        return {"success": False, "message": "No such user."}   

    data = database_helper.query_db("select * from users WHERE email=?", [email], one=True)
    match = {
        "email": data[0],
        "city": data[1],
        "country": data[2],
        "familyname": data[3],
        "firstname": data[4],
        "gender": data[5]
    }

    return {"success": True, "message": "User data retrieved.", "data": match};

@app.route("/post_message", methods=["POST"])
def post_message():
    """
    Tries to post a message to the wall of the user specified by the email address.
    """
    token = request.headers.get("token")
    message = request.headers.get("message")
    email = request.headers.get("email")
    
    if (not database_helper.query_db("SELECT * from users WHERE email=?", [email], one=True)):
        return {"success": False, "message": "No such user."}

    if (not database_helper.query_db("SELECT * from loggedinusers WHERE token=?", [token], one=True)):
        return {"success": False, "message": "You are not signed in."}

    database_helper.query_db("INSERT INTO messages(writer, content) VALUES(?, ?)", [email, message])
    return {"success": True, "message": "Message posted"}


@app.route("/get_user_messages_by_token", methods=["POST"])
def get_user_messages_by_token():
    """
    Retrieves the stored messages for the user whom the passed token is issued for. The
    currently signed in user can use this method to retrieve all its own messages from the server
    """
    token = request.headers.get("token")
    email = database_helper.query_db("SELECT email from loggedinusers WHERE token=?", [token], one=True)

    if (not email):
        return {"success": False, "message": "You are not signed in."}

    if (not database_helper.query_db("SELECT * from users WHERE email=?", [email[0]], one=True)):
        return {"success": False, "message": "No such user."}
    
    data = database_helper.query_db("select * from messages WHERE writer=?", [email[0]])

    match = []
    for message in data:
        match.append({
        "writer": message[0],
        "content": message[1],
    })
    return {"success": True, "message": "User messages retrieved.", "data": match};


@app.route("/get_user_messages_by_email", methods=["POST"])
def get_user_messages_by_email():
    """
    Retrieves the stored messages for the user specified by the passed email address.
    """
    token = request.headers.get("token")
    email = request.headers.get("email")

    if (not database_helper.query_db("SELECT * from loggedinusers WHERE token=?", [token], one=True)):
        return {"success": False, "message": "You are not signed in."}
    
    if (not database_helper.query_db("SELECT * from users WHERE email=?", [email], one=True)):
        return {"success": False, "message": "No such user."}

    data = database_helper.query_db("select * from messages WHERE writer=?", [email])

    match = []
    for message in data:
        match.append({
        "writer": message[0],
        "content": message[1],
    })
    return {"success": True, "message": "User messages retrieved.", "data": match};


@app.route("/print", methods=['GET'])
def test():
    """
    Only for debug.
    """
    for user in database_helper.query_db("select * from users"):
        print("User: ", user)

    for loggedinuser in database_helper.query_db("select * from loggedinusers"):
        print("Logged in user: ", loggedinuser)
    
    for message in database_helper.query_db("select * from messages"):
        print("Message: ", message)

    return {"success": True, "message": "Print done"}


    