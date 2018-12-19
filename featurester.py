from app import create_app, db
from app.models import Feature, Client, ProductArea


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Feature': Feature, 'Client': Client, 'ProductArea': ProductArea}
