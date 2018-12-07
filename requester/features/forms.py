from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField,SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class FeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client_priority = IntegerField('Client Priority')
    target_date = DateField('Target Date')
    client_id = SelectField('Client', choices=[], coerce=int)
    product_areas = SelectMultipleField('Product Areas', choices=[], coerce=int)
    submit = SubmitField('Add Request')
