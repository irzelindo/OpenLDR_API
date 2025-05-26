# This is an OpenLDR API running on python with flask_restx
# The production server is waitress running on port 9001
# The execution command is waitress-serve --host=127.0.0.1 --port=9001 app:app or waitress-serve --port=9001 app:app
# The service is served by nssm service manager
# Configure NSSM: In the NSSM GUI:
# Path: Set this to your Python interpreter path, e.g., C:\Users\Administrator\scripts\OpenLDR_API\.env\Scripts\python.exe
# Startup Directory: Set this to the directory where api.py is located, e.g., C:\Users\Administrator\scripts\OpenLDR_API\
# Arguments: Set this to run your Flask app using Waitress: -m waitress-serve --host=127.0.0.1 --port=9001 app:app
# or -m waitress-serve --port=9001 app:app
# The service name is OpenLDR_API to start, stop, or remove it refer to nssm --help command, e.g, nssm start OpenLDR_API
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
from waitress import serve


app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SWAGGER"] = {
    "title": "OpenLDR API",
    "uiversion": 3,
    # "openapi": "3.0.2",  # Ensure compatibility with Redoc
}

# print(SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ["tb"])

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
    # app.run()
    # serve(
    #     wsgiapp,
    #     host='127.0.0.1',
    #     port=5000
    # )
