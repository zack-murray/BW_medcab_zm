# web_app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask, Blueprint, render_template, Request

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.web_routes import web_routes

load_dotenv(override=True)
#DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgres://tfzioqkj:TkzyuAUgVfJwNwW8Nbh3xcVoo4T9vN2s@ruby.db.elephantsql.com:5432/tfzioqkj"

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(home_routes)
    app.register_blueprint(web_routes)
    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
