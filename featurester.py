"""Entry point for the application and for the WSGI Server"""
from flask_script import Manager
from app import create_app, db
from app.models import Feature, Client, ProductArea
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app()

manager = Manager(app)


@manager.command
def test(coverage=False):
    """Run the unit tests."""

    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(base_dir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://{}/index.html'.format(covdir))
        COV.erase()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Feature': Feature, 'Client': Client, 'ProductArea': ProductArea}


if __name__ == '__main__':
    manager.run()
