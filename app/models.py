from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    features = db.relationship('Feature', backref=db.backref('client'), cascade='all, delete-orphan',
                               lazy=True)

    def __init__(self, name, email, features=None):
        self.name = name
        self.email = email
        if features is None:
            self.features = []
        else:
            self.features = features

    def __repr__(self):
        return '<Client {}>'.format(self.name)


class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ProductArea  {}>'.format(self.name)


class Feature(db.Model):
    """Feature Table"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'client.id'), nullable=False)
    product_areas = db.relationship('ProductArea', secondary='product_areas', lazy='dynamic',
                                    backref=db.backref('features', lazy='dynamic'))

    def __init__(self, title, description, client_priority, target_date, client,
                 product_area=None):
        self.title = title
        self.description = description
        self.client_priority = client_priority
        self.target_date = target_date
        self.client_id = client.id
        if product_area is None:
            self.product_areas = []
        else:
            self.product_areas = product_area

    def __repr__(self):
        return '<Feature {}>'.format(self.title)


#  ProductArea helper table
product_areas = db.Table('product_areas',
                         db.Column('product_areas_id', db.Integer, db.ForeignKey(
                             'product_area.id'), primary_key=True),
                         db.Column('feature_id', db.Integer, db.ForeignKey(
                             'feature.id'), primary_key=True)
                         )
