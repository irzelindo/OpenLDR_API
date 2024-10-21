from flask import Flask
from flask_restful import Api
from flasgger import Swagger  # type: ignore
from flask_cors import CORS
from hiv.vl.routes import vl_routes
from dict.routes import dict_routes
from db.database import db
from configs.paths import *
from utilities.utils import *
from utilities.swagger import swagger_template


app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

api = Api(app)

# Initialize Swagger with the Template
# Access swagger UI by endpoint http://localhost:5000/apidocs/#/
swagger = Swagger(app, template=swagger_template)

db.init_app(app)

vl_routes(api)

dict_routes(api)


if __name__ == "__main__":
    app.run(debug=True)
