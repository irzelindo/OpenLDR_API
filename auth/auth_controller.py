import requests
from flask_restful import Resource, reqparse
from auth.auth_service import (
    login_user_service,
    get_all_users_service,
    update_user_service,
    delete_user_service,
    create_user_service,
    logout_user_service,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
# from configs.paths import *
from configs.paths_local import *


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
        current_user = get_jwt_identity() 

        # print(current_user)   

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        try:
            response = get_all_users_service(current_user)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )

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
            return jsonify(
                {
                    "status": 400,
                    "error": "Bad Request",
                    "message": "Username and password are required",
                }
            )
        try:
            response = login_user_service(args)

            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )

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
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

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

        try:
            response = update_user_service(args, current_user)

            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )

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
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        parser = reqparse.RequestParser()

        parser.add_argument("user_id", required=True)

        args = parser.parse_args()

        try:
            response = delete_user_service(args.user_id, current_user)

            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )


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
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        parser = reqparse.RequestParser()

        parser.add_argument("username", required=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("confirm_password", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("role", required=True)

        args = parser.parse_args()

        try:
            response = create_user_service(args, current_user)

            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )


class clerk_user_controller(Resource):
    def post(self):
        """
        Handle POST request from clerk user authentication webhook.
        ---
        tags:
            - Clerk/Webhook
        responses:
            200:
                description: Returns a success message webhook is received.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        data = request.get_json()

        # logging.info(data)

        headers = {
            "Authorization": f"Bearer {CLERK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        if not data:
            return jsonify(
                {
                    "status": 400,
                    "error": "Bad Request",
                    "message": "Invalid payload",
                }
            )

        if data:
            # return jsonify({"status": 200, "message": "Webhook Received"})
            try:
                event_type = data.get("type")

                if event_type == "session.removed":
                    # Request user from clerk API to get user details
                    user_id = data.get("data", {}).get("user_id")

                    status = data.get("data").get("status")

                    if status == "removed":
                        # Make request to clerk API
                        response = requests.get(
                            f"{CLERK_API_URL}/users/{user_id}", headers=headers
                        )

                    response = response.json()

                    args = {
                        "user_id": user_id,
                        "first_name": response.get("first_name"),
                        "last_name": response.get("last_name"),
                        "username": f"{response.get('first_name')}_{response.get('last_name')}",
                        "email": response.get("email_addresses", [{}])[0].get(
                            "email_address"
                        ),
                        "provider": "clerk",
                        "password": user_id,
                        "confirm_password": user_id,
                        "role": "user",
                    }

                    logout = logout_user_service(args)

                    return jsonify(
                        {
                            "status": 200,
                            "message": logout.get("message"),
                            "data": logout.get("data"),
                            "token": logout.get("token"),
                        }
                    )
                elif event_type == "session.ended":
                    # Request user from clerk API to get user details
                    user_id = data.get("data", {}).get("user_id")

                    status = data.get("data").get("status")

                    if status == "ended":
                        # Make request to clerk API
                        response = requests.get(
                            f"{CLERK_API_URL}/users/{user_id}", headers=headers
                        )

                    response = response.json()

                    args = {
                        "user_id": user_id,
                        "first_name": response.get("first_name"),
                        "last_name": response.get("last_name"),
                        "username": f"{response.get('first_name')}_{response.get('last_name')}",
                        "email": response.get("email_addresses", [{}])[0].get(
                            "email_address"
                        ),
                        "provider": "clerk",
                        "password": user_id,
                        "confirm_password": user_id,
                        "role": "user",
                    }

                    logout = logout_user_service(args)

                    return jsonify(
                        {
                            "status": 200,
                            "message": logout.get("message"),
                            "data": logout.get("data"),
                            "token": logout.get("token"),
                        }
                    )
                elif event_type == "user.created":
                    # Request user from clerk API to get user details
                    user_id = data.get("data", {}).get("id")

                    # Make request to clerk API
                    response = requests.get(
                        f"{CLERK_API_URL}/users/{user_id}", headers=headers
                    )

                    response = response.json()

                    args = {
                        "user_id": user_id,
                        "first_name": response.get("first_name"),
                        "last_name": response.get("last_name"),
                        "username": f"{response.get('first_name')}_{response.get('last_name')}",
                        "email": response.get("email_addresses", [{}])[0].get(
                            "email_address"
                        ),
                        "provider": "clerk",
                        "password": user_id,
                        "confirm_password": user_id,
                        "role": "user",
                    }

                    user_create = create_user_service(args, user_id)

                    return jsonify(
                        {
                            "status": 200,
                            "message": user_create.get("message"),
                            "data": user_create.get("data"),
                            "token": user_create.get("token"),
                        }
                    )
                elif event_type == "user.updated":
                    # Request user from clerk API to get user details
                    user_id = data.get("data", {}).get("id")

                    # Make request to clerk API
                    response = requests.get(
                        f"{CLERK_API_URL}/users/{user_id}", headers=headers
                    )

                    response = response.json()

                    args = {
                        "user_id": user_id,
                        "first_name": response.get("first_name"),
                        "last_name": response.get("last_name"),
                        "username": f"{response.get('first_name')}_{response.get('last_name')}",
                        "email": response.get("email_addresses", [{}])[0].get(
                            "email_address"
                        ),
                        "provider": "clerk",
                        "password": user_id,
                        "confirm_password": user_id,
                        "role": "user",
                    }

                    user_update = update_user_service(args, user_id)

                    return jsonify(
                        {
                            "status": 200,
                            "message": user_update.get("message"),
                            "data": user_update.get("data"),
                            "token": user_update.get("token"),
                        }
                    )
                elif event_type == "user.deleted":
                    # Request user from clerk API to get user details
                    user_id = data.get("data", {}).get("id")

                    deteled = delete_user_service(user_id)

                    return jsonify(
                        {
                            "status": 200,
                            "message": deteled.get("message"),
                            "data": deteled.get("data"),
                            "token": deteled.get("token"),
                        }
                    )
            except Exception as e:
                return jsonify(
                    {
                        "status": 500,
                        "error": "Internal Server Error",
                        "message": str(e),
                    }
                )
