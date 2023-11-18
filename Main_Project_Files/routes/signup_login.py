from flask import Flask, jsonify, request, Blueprint, session, render_template
#Import DB Functionality
from database_functionality.database_conn import *


# Initiating Blueprint
login_routes = Blueprint('login_routes', __name__)

createDB()

# Home Route
@login_routes.route('/')
def home():
    try:
        return render_template('index.html', User_Already_flag = False, Wrong_Password_flag=False)
    except Exception as e:
        return jsonify({"Error": str(e)})

@login_routes.route('/signup', methods = ['POST'])
def signup():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            
            if check_user_existence(email):
                return render_template('index.html', User_Already_flag = True, Wrong_Password_flag=False)
            else:
                try:
                    add_user(name, email, password)
                
                    return render_template('functionality.html', Signup_flag = True, Login_flag = False)
                except Exception as e:
                    return jsonify({"Error": str(e)})
        else:
            return jsonify({"Error": "POST Method Required"}) 
    except Exception as e:
        return jsonify({"Error" :str(e)})


@login_routes.route('/login', methods = ['POST'])
def login():
    try:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            if not is_password_correct(email, password):
                return render_template('index.html',User_Already_flag = False, Wrong_Password_flag=True )
            else:
                try:
                    return render_template('functionality.html', Signup_flag = False, Login_flag = True)  
                except Exception as e:
                    return jsonify({"Error": str(e)})   
        else:
            return jsonify({"Error": "POST Method Required"})
    except Exception as e:
        return jsonify({"Error": str(e)})   
        

                
@login_routes.route('/password', methods = ['GET'])
def renderForgotPassword():
    try:
        return render_template("forgotPasswordForm.html")
    except Exception as e:
        return jsonify({"Error": str(e)})

@login_routes.route('/setPassword', methods = ['POST'])
def setNewPassword():
    try:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')

            answerNewPassFunc = change_password(email, password)
            if isinstance(answerNewPassFunc, bool):
                if answerNewPassFunc == True:
                    return render_template('index.html', User_Already_flag = False, Wrong_Password_flag=False)
                else:
                    return render_template('index.html', User_Already_flag = False, Wrong_Password_flag=True)
            
            else:
                return jsonify({"Error" : str(answerNewPassFunc)})
    except Exception as e:
        return jsonify({"Error": str(e)})
    
@login_routes.route('/again')
def again():
    try:
        return render_template('functionality.html', Signup_flag = False, Login_flag = False)  
    except Exception as e:
        return jsonify({"Error": str(e)})