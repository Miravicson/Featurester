import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from requester import app, db, models
from requester.models import ProductArea, Feature, Client

app.config.from_object(os.environ['APP_SETTINGS'])

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()