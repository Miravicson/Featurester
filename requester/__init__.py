from requester import views
from wtforms import validators
from wtforms.ext.appengine.db import model_form
from flask_wtf import FlaskForm, Form
import os
from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from requester.features.forms import FeatureForm


# Initialize app
app = Flask(__name__)
# Configure app from settings attached to the environmet variable loaded from the .env file or production environment variable
app.config.from_object(os.environ['APP_SETTINGS'])




# initialise database
db = SQLAlchemy(app)
# Add bootstrap
Bootstrap(app)
# import the application views
# Register Blueprints


# Home Page route
@app.route('/')
@app.route('/home')
def index():

    form = FeatureForm(request.form)

    # print(form.errors)
    if request.method == 'POST':
        title=request.form['title']
        description=request.form['description']
        client_priority=request.form['client_priority']
        target_date = request.form['target_date']
        client_id = request.form['client_id']
        product_areas = request.form['product_areas']
        
        if form.validate():
           pass
        else:
            flash('Error: All Fields are Required')
    return render_template('index.html')



