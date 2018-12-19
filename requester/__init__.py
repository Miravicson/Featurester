import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from dotenv import load_dotenv
load_dotenv()

# Initialize app
app = Flask(__name__)
# Configure app from settings attached to the environment variable loaded from the .env

app.config.from_object(os.getenv('APP_SETTINGS'))


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
from requester.forms import FeatureForm, ClientForm, ProductAreaForm




@app.route('/', methods=['GET', 'POST'])
def index():
    """ The main view function, serves the home page of the dashboard and handles 3 forms for
    adding Features, adding Clients and adding Product Areas"""
    clients = Client.query.limit(3).all()
    products = ProductArea.query.order_by('id').limit(5).all()
    features = Feature.query.order_by('client_priority').limit(5).all()
    form = FeatureForm()
    # populate the list of clients for the add feature form
    form.client_id.choices = [(c.id, c.name) for c in clients]
    # populate the list of product areas for the add feature form
    form.product_areas.choices = [(p.id, p.name) for p in products]
    form2 = ClientForm()
    form3 = ProductAreaForm()

    def add_commit_feature(input_data):
        """takes forms data and create an instance of a feature adds to a session and makes commit"""

        product_areas_form = input_data.pop('product_areas', None)

        f = Feature(**input_data)
        if product_areas_form:
            product_areas = [ProductArea.query.get(i) for i in product_areas_form]
            for product_area in product_areas:
                product_area.features.append(f)
        db.session.add(f)
        db.session.commit()

    def get_feature_form_input():
        """Gets the input form data and packs it into a dictionary"""
        data = dict()
        data["title"] = form.title.data
        data["description"] = form.description.data
        data["target_date"] = form.target_date.data
        data['client_priority'] = form.client_priority.data
        data["client"] = Client.query.get(int(form.client_id.data))
        data["product_areas"] = form.product_areas.data
        return data

    if form.validate_on_submit():
        form_data = get_feature_form_input()
        priority = form_data.get('client_priority')
        client_id = form_data['client'].id

        # Get all the features belonging to the particular client
        client_features = db.session.query(Feature).filter(Feature.client_id == client_id).all()

        # when no feature has been added to the client, just add the feature
        if not client_features:
            add_commit_feature(form_data)
            app.logger.warning("I entered this if statement")

        # Add feature if the current client priority has not been taken.
        elif not list(filter(lambda x: x.client_priority == 1, client_features)):
            add_commit_feature(form_data)
        else:
            # Get all feature entries with priorities equal to or higher than the input priority
            equal_or_higher = sorted(filter(lambda x: x.client_priority >= priority, client_features),
                                     key=lambda x: x.client_priority)
            # create an accumulator to compare previous priorities of adjacent entries in an ordered
            #   list
            accumulator = list()
            for idx in range(0, len(equal_or_higher)):
                # for the first time in the list of equal or higher, check to see if there is an equal priority
                if idx == 0:
                    if equal_or_higher[idx].client_priority == priority:
                        accumulator.append(priority + 1)
                        equal_or_higher[idx].client_priority = priority + 1
                        db.session.add(equal_or_higher[idx])
                    else:
                        accumulator.append(equal_or_higher[idx].client_priority)
                elif equal_or_higher[idx].client_priority == accumulator[-1]:
                    accumulator.append(equal_or_higher[idx].client_priority + 1)
                    equal_or_higher[idx].client_priority = accumulator[-2] + 1
                    db.session.add(equal_or_higher[idx])
                else:
                    accumulator.append(equal_or_higher[idx].client_priority)
            add_commit_feature(form_data)

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


@app.route('/<int:client_id>', methods=['GET', 'POST'])
def client_details(client_id):
    client = Client.query.get_or_404(client_id)
    features = db.session.query(Feature).filter(Feature.client_id == client_id).order_by('client_priority').all()
    return render_template('features/client_details.html', client=client, features=features)