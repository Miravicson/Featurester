import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Initialize app
app = Flask(__name__)
# Configure app from settings attached to the environment variable loaded from the .env
#  file or production environment variable
app.config.from_object(os.environ['APP_SETTINGS'])

# initialise database
db = SQLAlchemy(app)
# Add bootstrap
Bootstrap(app)

# Add Flask Moment
moment = Moment(app)

# import the application views
from requester import views

#  Import the models
from requester.models import Feature, Client, ProductArea

# Import the form
from requester.features.forms import FeatureForm, ClientForm, ProductAreaForm


# Home Page route


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    clients = Client.query.limit(3).all()
    products = ProductArea.query.order_by('id').limit(5).all()
    features = Feature.query.order_by('id').limit(5).all()
    form = FeatureForm()
    form.client_id.choices = [(c.id, c.name) for c in clients]
    form.product_areas.choices = [(p.id, p.name) for p in products]
    form2 = ClientForm()
    form3 = ProductAreaForm()

    if form.validate_on_submit():
        data = dict()
        data["title"] = form.title.data
        data["description"] = form.description.data
        data["target_date"] = form.target_date.data
        priority = form.client_priority.data
        data['client_priority'] = priority
        client_id = form.client_id.data
        data["client"] = Client.query.get(int(client_id))
        product_areas = form.product_areas.data
        product_areas = [ProductArea.query.get(int(i)) for i in product_areas]
        f = Feature(**data)

        # check for clash of priority and update the older priorities , moving them down the chain
        c = Client.query.get(client_id)
        # higher_priority =
        # app.logger.warning(higher_priority)

        for product_area in product_areas:
            product_area.features.append(f)
        db.session.add(f)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash(form.errors)

    if form2.validate_on_submit():
        data = dict()
        data["name"] = form2.name.data
        data["email"] = form2.email.data
        c = Client(**data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash(form.errors)

    if form3.validate_on_submit():
        data = dict()
        data["name"] = form3.name.data
        p = ProductArea(**data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash(form.errors)

    return render_template('index.html', product_list=products, clients=clients, features=features, form=form,
                           form2=form2, form3=form3)
