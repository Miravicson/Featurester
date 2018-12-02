from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class FeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client_priority = IntegerField('Client Priority')
    target_date = DateField('Target Date')
    client_id = SelectField('Client', coerce=int)
    product_areas = SelectMultipleField('Product Areas')




""" Possible view function for  FeatureForm 


def edit_user(request, id):
    user = User.query.get(id)
    form = UserDetails(request.POST, obj=user)
    form.group_id.choices = [(g.id, g.name)
                              for g in Group.query.order_by('name')]

"""