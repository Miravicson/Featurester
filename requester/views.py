from requester import app
from flask import render_template

# Error handler views

@app.errorhandler(404)
def route_not_found(e):
    """Return a custom 404 Http response message for missing or not found routes"""

    code = 404
    return render_template('snippets/error.html', code=code), code
    

@app.errorhandler(405)
def method_not_found(e):
    """
    Custom response for methods not allowed for the requested URLs
    :param e: Exception
    :return:
    """
    code = 405
    return render_template('snippets/error.html', code=code), code


@app.errorhandler(500)
def internal_server_error(e):
    """
    Return a custom message for a 500 internal error
    :param e: Exception
    :return:
    """
    code = 500
    return render_template('snippets/error.html', code=code), code
    
