from flask import flash, redirect, render_template, url_for

from app import db
from app.models import Client, Feature, ProductArea

from . import bp
from .forms import ClientForm, FeatureForm, ProductAreaForm


@bp.route('/', methods=['GET'])
def landing():
    """ The Landing Page for the featurester application"""
    return render_template('landing.html')

@bp.route('/app', methods=['GET', 'POST'])
def index():
    """ The main view function, serves the home page of the dashboard and handles 3 forms for
    adding Features, adding Clients and adding Product Areas"""
    clients = Client.query.limit(3).all()
    products = ProductArea.query.order_by('id').limit(5).all()
    features = Feature.query.order_by('client_priority').limit(5).all()
    feature_form = FeatureForm()
    feature_form.populate_choices()
    client_form = ClientForm()
    product_form = ProductAreaForm()

    if feature_form.submit_feature.data and feature_form.validate():
        # Get the form data
        form_data = feature_form.get_data()
        # process the form data and check for existing client priority and reorder the priorities of older features if there is a clash of priorities
        Feature.save_sort_algo(form_data, db)

        return redirect(url_for('main.index'))

    if client_form.submit_client.data and client_form.validate():
        data = dict()
        data["name"] = client_form.name.data
        data["email"] = client_form.email.data
        c = Client(**data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('main.index'))

    if product_form.submit_product.data and product_form.validate():
        data = dict()
        data["name"] = product_form.name.data
        p = ProductArea(**data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('index.html', product_list=products, clients=clients, features=features,
                           feature_form=feature_form,
                           client_form=client_form, product_form=product_form)


@bp.route('/<int:client_id>', methods=['GET', 'POST'])
def client_details(client_id):
    client = Client.query.get_or_404(client_id)
    features = db.session.query(Feature).filter(
        Feature.client_id == client_id).order_by('client_priority').all()
    return render_template('client_details.html', client=client, features=features)


@bp.route('/delete_feature/<int:client_id>/<int:feature_id>', methods=['GET', 'POST'])
def delete_features(client_id, feature_id):
    feature = Feature.query.get_or_404(feature_id)
    feature.product_areas = []
    db.session.add(feature)
    db.session.commit()
    db.session.delete(feature)
    db.session.commit()
    return redirect(url_for('main.client_details', client_id=client_id))


@bp.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('main.index'))
