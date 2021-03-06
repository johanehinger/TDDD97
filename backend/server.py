from flask import Flask, request
import database_helper
import math
import random
# TODO: JSON instead of headers.
# TODO: token as auth in postman
# TODO: create helper functions for all queries.

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
    email = request.json.get("email")
    password = request.json.get("password")

    # Assert that the user does exist and that the password is correct!
    if (not database_helper.get_specific_user(email, password)):
        return {"success": False, "message": "Wrong username or password."};
    
    token = generateToken()
    # database_helper.query_db("INSERT INTO loggedinusers(token, email) VALUES(?, ?)", [token, email])
    database_helper.add_user(token, email)
    return {"success": True, "message": "Successfully signed in.", "data": token }

@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Registers a user in the database.
    """
    firstName = request.json.get("firstname")
    familyName = request.json.get("familyname")
    gender = request.json.get("gender")
    city = request.json.get("city")
    country = request.json.get("country")
    email = request.json.get("email")
    password = request.json.get("password")
    print(firstName)
    print(not (firstName and familyName and gender and city and country))
    print(not ('@' in email))
    
    # Assert that the user doesn't exist.
    if (database_helper.select_user_by_email(email) != None):
        return {"success": False, "message": "User already exists."}

    # Data must be valid
    if (not (firstName and familyName and gender and city and country) or (len(password)<5) or not ('@' in email)):
        return {"success": False, "message": "Form data missing or incorrect type."};
    database_helper.create_user(email, city, country, familyName, firstName, gender, password)
    return {"success": True, "message": "Successfully created a new user."};


@app.route("/sign_out", methods=["POST"])
def sign_out():
    """
    Signs out a user from the system.
    """
    token = request.headers.get("Authorization").split()[1]
    
    if (not database_helper.select_user_by_token(token)):
        return {"success": False, "message": "You are not signed in."}
    
    database_helper.remove_user(token)
    return {"success": True, "message": "Successfully signed out."}


@app.route("/change_password", methods=["PUT"])
def change_password():
    """
    Changes the password of the current user to a new one.
    """
    token = request.headers.get("Authorization").split()[1]
    oldPassword = request.json.get("oldpassword")
    newPassword = request.json.get("newpassword")
    email = database_helper.select_user_by_token(token)

    if (not email):
        return {"success": False, "message": "You are not logged in."} 

    if (not database_helper.get_specific_user(email[1], oldPassword)):
        return {"success": False, "message": "Wrong password."}

    database_helper.set_password(email[1], newPassword)
    return {"success": True, "message": "Password changed."}


@app.route("/get_user_data_by_token", methods=["GET"])
def get_user_data_by_token():
    """ 
    Retrieves the stored data for the user whom the passed token is issued for. The currently
    signed in user can use this method to retrieve all its own information from the server
    """
    token = request.headers.get("Authorization").split()[1]
    email = database_helper.get_email_by_token(token)

    if (not email):
        return {"success": False, "message": "You are not signed in."}

    user = database_helper.get_user_by_email(email[0])

    if (not user):
        return {"success": False, "message": "No such user."}   

    data = database_helper.select_user_by_email(email[0])
    match = {
        "email": data[0],
        "city": data[1],
        "country": data[2],
        "familyname": data[3],
        "firstname": data[4],
        "gender": data[5]
    }

    return {"success": True, "message": "User data retrieved.", "data": match};


@app.route("/get_user_data_by_email", methods=["GET"])
def get_user_data_by_email():
    """
    Retrieves the stored data for the user specified by the passed email address.
    """
    token = request.headers.get("Authorization").split()[1]
    email = request.args.get('email')

    if (not database_helper.select_user_by_token(token)):
        return {"success": False, "message": "You are not signed in."}

    user = database_helper.select_user_by_email(email)
    print(user)
    if (not user):
        return {"success": False, "message": "No such user."}   

    data = database_helper.select_user_by_email(email)
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
    token = request.headers.get("Authorization").split()[1]
    message = request.json.get("message")
    email = request.json.get("email")
    
    if (not database_helper.select_user_by_email(email)):
        return {"success": False, "message": "No such user."}

    if (not database_helper.select_user_by_token(token)):
        return {"success": False, "message": "You are not signed in."}

    database_helper.create_message(email, message)
    return {"success": True, "message": "Message posted"}


@app.route("/get_user_messages_by_token", methods=["GET"])
def get_user_messages_by_token():
    """
    Retrieves the stored messages for the user whom the passed token is issued for. The
    currently signed in user can use this method to retrieve all its own messages from the server
    """
    token = request.headers.get("Authorization").split()[1]
    email = database_helper.get_email_by_token(token)

    if (not email):
        return {"success": False, "message": "You are not signed in."}

    if (not database_helper.get_user_by_email(email[0])):
        return {"success": False, "message": "No such user."}
    
    data = database_helper.get_messages_by_email(email[0])

    match = []
    for message in data:
        match.append({
        "writer": message[0],
        "content": message[1],
    })
    return {"success": True, "message": "User messages retrieved.", "data": match};


@app.route("/get_user_messages_by_email", methods=["GET"])
def get_user_messages_by_email():
    """
    Retrieves the stored messages for the user specified by the passed email address.
    """
    token = request.headers.get("Authorization").split()[1]
    email = request.args.get('email')


    if (not database_helper.select_user_by_token(token)):
        return {"success": False, "message": "You are not signed in."}
    
    if (not database_helper.select_user_by_email(email)):
        return {"success": False, "message": "No such user."}

    data = database_helper.get_messages_by_email(email)

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


    