from requester import db
from sqlalchemy.dialects.postgresql import JSON

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    features = db.relationship('Feature', backref='client', lazy=True)

    def __repr__(self):
        return '<Client {}>'.format(self.name)

class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    feature = db.relationship('Feature', secondary='product_areas', lazy='subquery',
                              backref=db.backref('product_area', lazy=True))
    def __repr__(self):
        return '<ProductArea  {}>' .format(self.name)

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_priority = db.Column(db.Integer, nullable=True)
    target_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'client.id'), nullable=False)
    product_areas = db.relationship('ProductArea', secondary=product_areas, lazy='subquery',
                                    backref=db.backref('features', lazy=True))
    def __repr__(self):
        return '<Feature {}>'.format(self.title)

#  ProductArea helper table
product_areas = db.Table('product_areas',
                         db.Column('product_areas_id', db.Integer, db.ForeignKey(
                             'product_area.id'), primary_key=True),
                         db.Column('feature_id', db.Integer, db.ForeignKey(
                             'feature.id'), primary_key=True)
                         )
