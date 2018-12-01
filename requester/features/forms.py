from flask_wtf import FlaskForm, Form
from wtforms.ext.appengine.db import model_form
from wtforms import validators
from requester.models import Feature

FeatureForm = model_form(Feature, Form, field_args={
    'name': {
        'validators': [validators.Length(max=10)]
    }
})
