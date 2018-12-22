from app.models import Client, Feature, ProductArea


def get_feature_form_input(form):
    """Gets the input form data and packs it into a dictionary"""
    data = dict()
    data["title"] = form.title.data
    data["description"] = form.description.data
    data["target_date"] = form.target_date.data
    data['client_priority'] = form.client_priority.data
    data["client"] = Client.query.get(int(form.client_id.data))
    data["product_areas"] = form.product_areas.data
    return data


def add_commit_feature(input_data, db):
    """takes forms data and create an instance of a feature adds to a session and makes commit"""

    product_areas_form = input_data.pop('product_areas', None)

    f = Feature(**input_data)
    if product_areas_form:
        product_areas = [ProductArea.query.get(i) for i in product_areas_form]
        for product_area in product_areas:
            product_area.features.append(f)
    db.session.add(f)
    db.session.commit()


def process_feature_form(db, form_data):
    """ An algorithm for sorting the features per client and ensuring that no two features have the same priority.
    it takes in the form data from the feature form and db """

    priority = form_data.get('client_priority')
    client_id = form_data['client'].id

    # Get all the features belonging to the particular client
    client_features = db.session.query(Feature).filter(Feature.client_id == client_id).all()

    # when no feature has been added to the client, just add the feature
    if not client_features:
        add_commit_feature(form_data, db)

    # Add feature if the current client priority has not been taken.
    elif not list(filter(lambda x: x.client_priority == 1, client_features)):
        add_commit_feature(form_data, db)
    else:
        # Get all feature entries with priorities equal to or higher than the input priority
        equal_or_higher = sorted(filter(lambda x: x.client_priority >= priority, client_features),
                                 key=lambda x: x.client_priority)
        # create an accumulator to compare previous priorities of adjacent entries in an ordered
        #   list
        accumulator = list()
        for idx in range(0, len(equal_or_higher)):
            # for the first time in the list of equal or higher, check to see if there is an equal priority
            if idx == 0:
                if equal_or_higher[idx].client_priority == priority:
                    accumulator.append(priority + 1)
                    equal_or_higher[idx].client_priority = priority + 1
                    db.session.add(equal_or_higher[idx])
                else:
                    accumulator.append(equal_or_higher[idx].client_priority)
            elif equal_or_higher[idx].client_priority == accumulator[-1]:
                accumulator.append(equal_or_higher[idx].client_priority + 1)
                equal_or_higher[idx].client_priority = accumulator[-2] + 1
                db.session.add(equal_or_higher[idx])
            else:
                accumulator.append(equal_or_higher[idx].client_priority)
        add_commit_feature(form_data, db)
