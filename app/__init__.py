import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# instantiate db object

db = SQLAlchemy()

migrate = Migrate()

bootstrap = Bootstrap()
moment = Moment()

config = os.getenv('APP_SETTINGS')


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


#  Import the models
from app import models

