import json
from flask_restful import Resource, reqparse
from auth.auth_service import (
    login_user_service,
    get_all_users_service,
    update_user_service,
    delete_user_service,
    create_user_service,
    clerk_user_service,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from flask import request
import requests

from configs.paths import *

# from configs.paths_local import *


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
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )
        if current_user.get("role") != "admin":
            return jsonify(
                {
                    "status": 403,
                    "error": "Forbidden",
                    "message": "User does not have permission to get all users",
                }
            )
        try:
            response = get_all_users_service(id)
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
        current_user = json.loads(get_jwt_identity())

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        if current_user.get("role") != "admin":
            return jsonify(
                {
                    "status": 403,
                    "error": "Forbidden",
                    "message": "User does not have permission to update",
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

        id = current_user.get("user_id")

        try:
            response = update_user_service(args, id)

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
        current_user = json.loads(get_jwt_identity())

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        if current_user.get("role") != "admin":
            return jsonify(
                {
                    "status": 403,
                    "error": "Forbidden",
                    "message": "User does not have permission to delete",
                }
            )

        parser = reqparse.RequestParser()

        parser.add_argument("user_id", required=True)

        args = parser.parse_args()

        id = current_user.get("user_id")

        try:
            response = delete_user_service(args, id)

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
        current_user = json.loads(get_jwt_identity())

        if not current_user:
            return jsonify(
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "User not authenticated",
                }
            )

        if current_user.get("role") != "admin":
            return jsonify(
                {
                    "status": 403,
                    "error": "Forbidden",
                    "message": "User does not have permission to create",
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

        current_user = json.loads(get_jwt_identity())

        args = parser.parse_args()

        id = current_user.get("user_id")

        try:
            response = create_user_service(args, id)

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
    # This function handles the POST request
    # From clerk authentication webhook
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
        clerk_payload = request.get_json(force=True)

        if not clerk_payload:
            return jsonify(
                {
                    "status": 400,
                    "error": "Bad Request",
                    "message": "Invalid payload",
                }
            )

        if clerk_payload:
            return jsonify({"status": 200, "message": "Webhook Received"})

        try:
            event_type = clerk_payload.get("type")

            if event_type == "session.created":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("Session Created", response.json())

            elif event_type == "session.removed":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("Session Removed", response.json())

            elif event_type == "session.ended":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("Session Ended", response.json())

            elif event_type == "user.created":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("User Created", response.json())

            elif event_type == "user.updated":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("User Updated", response.json())

            elif event_type == "user.deleted":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                response = requests.get(
                    f"{CLERK_API_URL}/users/{user_id}", headers=headers
                )

                # Print response
                print("User Deleted", response.json())

                # Print Deleted User ID
                print(user_id)

            elif event_type == "email.created":
                # Request user from clerk API to get user details
                user_id = clerk_payload.get("data", {}).get("user_id")

                headers = {
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json",
                }

                # Make request to clerk API
                # response = requests.get(
                #     f"{CLERK_API_URL}/users/{user_id}", headers=headers
                # )

                # Print response
                # print("Email Created", response.json())

                print("Email Created", clerk_payload)

        except Exception as e:
            return jsonify(
                {
                    "status": 500,
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            )
