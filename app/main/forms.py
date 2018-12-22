from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email
from app.models import ProductArea, Client


class FeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client_priority = IntegerField('Client Priority')
    target_date = DateField('Target Date')
    client_id = SelectField('Client', choices=[], coerce=int)
    product_areas = SelectMultipleField(
        'Product Areas', choices=[], coerce=int)
    submit_feature = SubmitField('Add Request')

    def populate_choices(self):
        """ Populates the ProductArea multiple fields options for the feature form"""

        clients = Client.query.all()
        self.client_id.choices = [(c.id, c.name) for c in clients]
        products = ProductArea.query.order_by('id').all()
        self.product_areas.choices = [(p.id, p.name) for p in products]


class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_client = SubmitField('Create Client')


class ProductAreaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit_product = SubmitField('Add Product Areas')
