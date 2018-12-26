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

    def get_data(self):
        """Gets the input form data and packs it into a dictionary"""
        data = dict()
        data["title"] = self.title.data
        data["description"] = self.description.data
        data["target_date"] = self.target_date.data
        data['client_priority'] = self.client_priority.data
        data["client"] = Client.query.get(int(self.client_id.data))
        data["product_areas"] = self.product_areas.data
        return data


    
    


class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_client = SubmitField('Create Client')


class ProductAreaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit_product = SubmitField('Add Product Areas')
