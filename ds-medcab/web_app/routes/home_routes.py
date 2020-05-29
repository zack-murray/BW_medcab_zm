# web_app/routes/home_routes.py

from flask import Blueprint
from flask import jsonify

# from web_app.all_names import all_names

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def hello():

    return ("Hello World!")


@home_routes.route("/jsontest")
def jsontest():
    data = {'test': 'success!'}
    return jsonify(data)


#@home_routes.route('/names')
#def get_all_strains():
    #data = all_names()
    #return jsonify(data)
