import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from requester.features.forms import FeatureForm
# Initialize app
app = Flask(__name__)
# Configure app from settings attached to the environmet variable loaded from the .env file or production environment variable
app.config.from_object(os.environ['APP_SETTINGS'])



# initialise database

db = SQLAlchemy(app)

# Add bootstrap
Bootstrap(app)

# import the application views

from requester import views


# Register Blueprints




# Home Page route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')



