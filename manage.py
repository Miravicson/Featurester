""" Manager for performing common tasks"""

import os
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True,
                            include='app/*',
                            omit=['app/errors/__init__.py', 'app/main/__init__.py'])
    COV.start()
app = create_app()

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""

    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        cov_dir = os.path.join(base_dir, 'tmp/coverage')
        COV.html_report(directory=cov_dir)
        print('HTML version: file://{}/index.html'.format(cov_dir))
        COV.erase()


if __name__ == '__main__':
    manager.run()
