import json
from flask_restful import Resource, reqparse
from auth.auth_service import (
    login_user_service,
    get_all_users_service,
    update_user_service,
    delete_user_service,
    create_user_service,
)
from flask_jwt_extended import jwt_required, get_jwt_identity


class user_controller(Resource):
    """
    Class to handle user login, update, and deletion.
    """

    @jwt_required()
    def get(self):
        """
        Handle GET request all users
        ---
        tags:
            - Authentication
        security:
            - Bearer: []
        responses:
            200:
                description: Returns a list of all users.
            401:
                description: Unauthorized
            500:
                description: An Error Occurred
        """
        current_user = json.loads(get_jwt_identity())
        id = current_user.get("user_id")
        if not current_user:
            return {"message": "User not authenticated"}, 401
        if current_user.get("role") != "admin":
            return {"message": "User does not have permission to retrieve users"}, 403
        try:
            return get_all_users_service(id), 200
        except Exception as e:
            return {"message": str(e)}, 500

    def post(self):
        """
        Handle POST request for user login.
        Expects 'username' and 'password' in the request body.
        ---
        tags:
            - Authentication
        parameters:
            - $ref: '#/parameters/UserLoginParameters'
        responses:
            200:
                description: Returns a JWT token if login is successful.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occurred
        """
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()
        if not args.get("username") or not args.get("password"):
            return {"message": "username and password are required"}, 400
        try:
            return login_user_service(args), 200
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def put(self):
        """
        Handle PUT request for user update.
        Expects 'username', first_name', 'last_name', 'user_id', 'email', 'role', and optional 'password' and 'confirm_password' in the request body.
        ---
        tags:
            - Authentication
        security:
            - Bearer: []
        parameters:
            - $ref: '#/parameters/UserUpdateParameters'
        responses:
            200:
                description: Returns the updated user details.
            400:
                description: Invalid Parameters
            401:
                description: Unauthorized
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        current_user = json.loads(get_jwt_identity())
        if not current_user:
            return {"message": "User not authenticated"}, 401
        if current_user.get("role") != "admin":
            return {"message": "User does not have permission to update"}, 403
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("user_id", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("role", required=True)
        parser.add_argument("password", required=False, default=None)
        parser.add_argument("confirm_password", required=False, default=None)
        args = parser.parse_args()
        id = current_user.get("user_id")
        try:
            return update_user_service(args, id), 200
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def delete(self):
        """
        Handle DELETE request for user deletion.
        Expects 'user_id' in the request body.
        ---
        tags:
            - Authentication
        security:
            - Bearer: []
        parameters:
            - $ref: '#/parameters/UserDeletionParameters'
        responses:
            200:
                description: Returns a success message if deletion is successful.
            400:
                description: Invalid Parameters
            401:
                description: Unauthorized
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        current_user = json.loads(get_jwt_identity())
        if not current_user:
            return {"message": "User not authenticated"}, 401
        if current_user.get("role") != "admin":
            return {"message": "User does not have permission to delete"}, 403
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        args = parser.parse_args()
        id = current_user.get("user_id")
        try:
            return delete_user_service(args, id), 200
        except Exception as e:
            return {"message": str(e)}, 500


class user_create_controller(Resource):
    @jwt_required()
    def post(self):
        """
        Handle POST request for user creation.
        Expects 'username', 'password', 'confirm_password', 'email', and 'role' in the request body.
        ---
        tags:
            - Authentication
        parameters:
            - $ref: '#/parameters/UserCreateParameters'
        responses:
            200:
                description: Returns a success message if user is created successfully.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        # current_user = json.loads(get_jwt_identity())
        # if not current_user:
        #     return {"message": "User not authenticated"}, 401
        # if current_user.get("role") != "admin":
        #     return {"message": "User does not have permission to create"}, 403
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("confirm_password", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("role", required=True)
        current_user = json.loads(get_jwt_identity())
        args = parser.parse_args()
        id = current_user.get("user_id")
        try:
            return create_user_service(args, id), 200
        except Exception as e:
            return {"message": str(e)}, 500
