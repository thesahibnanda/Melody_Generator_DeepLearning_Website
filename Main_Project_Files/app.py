from flask import Flask

# Import Routes
from routes.signup_login import login_routes
from routes.file_management import file_routes

# Initiating App
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(login_routes) 
app.register_blueprint(file_routes)

if __name__ == "__main__":
    app.run(debug=True)