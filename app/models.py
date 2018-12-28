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
    client_priority = db.Column(db.Integer, nullable=False, index=True)
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

    @staticmethod
    def add_commit_feature(form_data, db):
        """takes forms data and create an instance of a feature adds to a session and makes commit"""

        product_areas_data = form_data.pop('product_areas', None)

        f = Feature(**form_data)
        if product_areas_data:
            product_areas = [ProductArea.query.get(
                i) for i in product_areas_data]
            for product_area in product_areas:
                product_area.features.append(f)
        db.session.add(f)
        db.session.commit()

    @staticmethod
    def save_sort_algo(form_data, db):
        """ An algorithm for sorting the features per client and ensuring that no two features have the same priority.
        it takes in the form data from the feature form and db """

        priority = form_data.get('client_priority')
        client_id = form_data['client'].id

        # Get all the features belonging to the particular client
        client_features = db.session.query(Feature).filter(
            Feature.client_id == client_id).all()

        # when no feature has been added to the client, just add the feature
        if not client_features:
            Feature.add_commit_feature(form_data, db)

        # Add feature if the current client priority has not been taken.

        elif priority not in [feature.client_priority for feature in client_features]:
            Feature.add_commit_feature(form_data, db)

        else:
            # Get all feature entries with priorities equal to or higher than the input priority
            equal_or_higher = sorted(
                (feature for feature in client_features if feature.client_priority >= priority))

            # create an accumulator to compare previous priorities of adjacent entries in an ordered list
            accumulator = list()
            for idx in range(0, len(equal_or_higher)):
                # check if the priority of the first feature is equal to the current priority
                if idx == 0:
                    if equal_or_higher[idx].client_priority == priority:
                        # if the priorities compared are equal, increase the priority of the first element in the list by one and add it to session
                        equal_or_higher[idx].client_priority = priority + 1
                        accumulator.append(
                            equal_or_higher[idx].client_priority)
                        db.session.add(equal_or_higher[idx])
                    else:
                        # if the priorities are not equal, just add the priority to the accumulator for the next comparison
                        accumulator.append(
                            equal_or_higher[idx].client_priority)
                # compare the priority of the next feature in the list with the last priority in the accumulator,
                elif equal_or_higher[idx].client_priority == accumulator[-1]:
                    # if the priorities compared are equal,
                    equal_or_higher[idx].client_priority = accumulator[-1] + 1 #increase the priority of the feature by one
                    accumulator.append(
                        equal_or_higher[idx].client_priority) # append this new priority to the accumulator for next comparison
                    db.session.add(equal_or_higher[idx])      # add the modified feature with new priority to session for later commit
                else:
                    # if the priorities are not equal, 
                    # just add the priority to the accumulator for the next comparison
                    accumulator.append(equal_or_higher[idx].client_priority)
            Feature.add_commit_feature(form_data, db) # create the new feature and commit the sessions


#  ProductArea helper table
product_areas = db.Table('product_areas',
                         db.Column('product_areas_id', db.Integer, db.ForeignKey(
                             'product_area.id'), primary_key=True),
                         db.Column('feature_id', db.Integer, db.ForeignKey(
                             'feature.id'), primary_key=True)
                         )
