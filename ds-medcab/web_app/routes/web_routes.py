# web_app/routes/web_routes.py

import pandas as pd
from flask import Blueprint, render_template, request, jsonify
from web_app.models import db, parse_records, Strains
from web_app.services.model_service import Model, Transformer
from os import path
from flask_cors import cross_origin
import pickle

web_routes = Blueprint("web_routes", __name__)


@web_routes.route("/add_strain", methods=['POST'])
@cross_origin()
def add_strain():
    """
    Endpoint takes parameters sent in a post request and passes
    them to a model to include new/additional strains based on the arguments
    that were passed by the user.
    """
    strain_data = request.get_json()
    new_strain = Strains(name=strain_data['name'], race=strain_data['race'],
                         flavors=strain_data['flavors'], positive=strain_data['positive'],
                         negative=strain_data['negative'], medical=strain_data['medical'],
                         description=strain_data['description'])

    db.session.add(new_strain)
    db.session.commit()

    return 'Strain added', 201


@web_routes.route('/products/fetch')
@cross_origin()
def get_strains():
    """
    Function/endpoint returns all of the entries in the database.
    """
    db_strains = Strains.query.all()
    response = parse_records(db_strains)
    return jsonify(response)


@web_routes.route('/strains/predict', methods=['GET', 'POST'])
@cross_origin()
def search_strains():

    # init the model
    model = Model
    pickle_off = open("web_app/transformer.pickle","rb")
    transformer = pickle.load(pickle_off)

    flavors = request.form['flavors']
    race = request.form['race']
    medical = request.form['medical'] 

    df = pd.Dataframe(data=[flavors, race, medical], columns=['flavors', 'race', 'medical'])
    dtm = transformer.transform(df)
    response = model.predict(dtm)
    return jsonify(response)


@web_routes.route('/products/predict', methods=['POST', 'GET'])
@cross_origin()
def predict_strains():

    tr = Transformer
    pickle_off = open("web_app/model.pickle", "rb")
    model = pickle.load(pickle_off)
    # model = Model.load_pickle("web_app/model.pickle")
    negitive = ['negitive']
    ignore = ['index', 'id']

    #name = request.form['name']
    #race = request.form['race']
    #flavors = request.form['flavors']
    #negative = request.form['negative']
    #positive = request.form['positive']
    #medical = request.form['medical']
    #description = request.form['description']
    #preference = request.form['preference']

    thisdict = { "name": 'Afpak',
                 "race": 'sativa',
                 "flavors": 'citrus',
                 "negitive": '',
                 "positive": 'relaxed',
                 "medical": 'depression',
                 "description": '',
                 "preference": ''}

    index = [0]
    df = pd.DataFrame(data=thisdict, index=index)
    #df = pd.DataFrame(data=[name, race, flavors, negative, positive, medical, description, preference],
                      #columns=['name', 'race', 'flavors', 'negative', 'positive', 'medical', 'description', 'preference'])
    user_transformed = tr.transform(document=df, ignore=ignore, negitive=negitive)
    #user_transformed = tr.transform(pd.DataFrame({'name': str,
                                                #  'race': str,
                                                #  'flavors': list,
                                                #  'negative': list,
                                                #  'positive': list,
                                                #  'medical': list,
                                                #  'description': str,
                                                #  'preference': list
                                            #    }),
                                #    negative,
                                #    ignore)
    pred = model.predict(user_transformed)
    return jsonify(pred[1])
