from flask import Flask, redirect
from flask_restful import Api
from flasgger import Swagger  # type: ignore
from flask_cors import CORS  # type: ignore
from hiv.vl.routes import vl_routes
from dict.routes import dict_routes
from tb.gxpert.routes import tb_gxpert_routes
from db.database import db
from configs.paths import *
from utilities.utils import *
from utilities.swagger import swagger_template


app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SWAGGER"] = {
    "title": "OpenLDR API",
    "uiversion": 3,
    # "openapi": "3.0.2",  # Ensure compatibility with Redoc
}

CORS(app)

api = Api(app)

# Initialize Swagger with the Template
# Access swagger UI by endpoint http://localhost:5000/apidocs/#/
swagger = Swagger(app, template=swagger_template)

db.init_app(app)

vl_routes(api)

tb_gxpert_routes(api)

dict_routes(api)


# Redirect the root URL to /apidocs/
@app.route("/")
def root():
    return redirect("/apidocs/")


if __name__ == "__main__":
    app.run(debug=True)
