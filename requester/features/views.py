from flask import Blueprint, request, abort


# Initialize blueprint
feature = Blueprint('feature', __name__)





@feature.route('/add-feature', methods=['GET', 'POST'])
def add_feature():
    pass
    # title = None
    # form = FeatureForm()
    # if form.validate_on_submit():
    #     title = form.title.data
    # return render_template('add_feature.html', form=form, title=title)
