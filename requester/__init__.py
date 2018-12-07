from wtforms import validators
from wtforms.ext.appengine.db import model_form
from flask_wtf import FlaskForm, Form
import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import datetime
f


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
#  Import the models
from requester.models import Feature, Client, ProductArea
# Import the from
from requester.features.forms import FeatureForm
# Home Page route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
        clients = Client.query.limit(3).all()
        products = ProductArea.query.limit(5).all()
        features = Feature.query.all()
        form = FeatureForm()
        form.client_id.choices= [(c.id, c.name) for c in clients]
        form.product_areas.choices = [(p.id, p.name) for p in products]

        if form.validate_on_submit():
                data = {}
                data["title"] = form.title.data
                data["description"] = form.description.data
                data["target_date"] = form.target_date.data
                data['client_priority'] = form.client_priority.data
                client_id = form.client_id.data
                data["client"] = Client.query.get(int(client_id))
                product_areas = form.product_areas.data
                product_areas = [ProductArea.query.get(int(i)) for i in product_areas]
                f = Feature(**data)
                for product_area in product_areas:
                        product_area.features.append(f)
                db.session.add(f)
                db.session.commit()
                return redirect(url_for('index'))
        else:
                flash(form.errors)
        return render_template('index.html', product_list = products, clients=clients, features=features, form=form)



