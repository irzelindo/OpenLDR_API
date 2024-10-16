from flask import Flask
from hiv.vl.routes import vl_routes, dict_routes
from db.database import db
from configs.paths import *
from utilities.utils import *
from flask_restful import Api


app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

db.init_app(app)

vl_routes(api)

dict_routes(api)


if __name__ == "__main__":
    app.run(debug=True)
