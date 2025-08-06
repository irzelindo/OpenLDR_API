import json
import bcrypt
import logging
from flask_jwt_extended import create_access_token
from flask import request
from auth.user_model import User, UserLogs
from uuid import uuid4
from datetime import datetime
from db.database import db

from configs.paths import *

# from configs.paths_local import *


def login_user_service(args):

    login_username = args.get("username")
    login_email = args.get("email")
    login_password = args.get("password")
    login_user_id = args.get("user_id")
    login_provider = args.get("provider")

    if login_username:
        user_query = User.query.filter_by(user_name=login_username).first()
    elif login_user_id:
        user_query = User.query.filter_by(user_id=login_user_id).first()
    else:
        user_query = User.query.filter_by(email=login_email).first()

    if not user_query or not bcrypt.checkpw(
        login_password.encode("utf-8"), user_query.password.encode("utf-8")
    ):
        if login_provider == "clerk":
            create_user_service(args, login_user_id)
        else:
            return (
                {
                    "status": 401,
                    "error": "Unauthorized",
                    "message": "Invalid credentials",
                },
            )

    user_query.last_login = datetime.now()

    # Store values before commit
    user_id = user_query.user_id
    user_name = user_query.user_name
    user_first_name = user_query.first_name
    user_last_name = user_query.last_name
    user_email = user_query.email
    role = get_user_role(user_query)

    db.session.commit()

    access_token = create_access_token(
        identity=json.dumps(
            {
                "username": user_name,
                "first_name": user_first_name,
                "last_name": user_last_name,
                "role": role,
                "user_id": user_id,
                "email": user_email,
            }
        )
    )

    try:
        save_user_log_service(
            {
                "user_id": user_id,
                "log_type": "login",
                "log_details": {
                    "user_id": user_id,
                    "user_name": user_name,
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "role": role,
                },
            }
        )
    except Exception as e:
        db.session.rollback()
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    return {
        "message": "Login successful",
        "data": {
            "user_id": user_id,
            "username": user_name,
            "first_name": user_first_name,
            "last_name": user_last_name,
            "email": user_email,
            "role": role,
        },
        "token": access_token,
        "status": 200,
    }


def get_user_role(user_query):
    if user_query:
        return user_query.role if hasattr(user_query, "role") else "user"
    return "guest"


def update_user_service(args, id):
    update_username = args.get("username")
    update_first_name = args.get("first_name")
    update_last_name = args.get("last_name")
    update_password = args.get("password")
    update_confirm_password = args.get("confirm_password")
    update_email = args.get("email")
    update_role = args.get("role")
    update_user_id = args.get("user_id")

    # print(id)

    if not all(
        [
            update_username,
            update_first_name,
            update_last_name,
            update_password,
            update_confirm_password,
            update_email,
            update_role,
            update_user_id,
        ]
    ):
        return ({"status": 400, "error": "Bad Request", "message": "Invalid input"},)

    if update_password != update_confirm_password:
        return (
            {
                "status": 400,
                "error": "Bad Request",
                "message": "Passwords do not match",
            },
        )

    user_query = User.query.filter_by(user_id=update_user_id).first()

    if not user_query:
        return {"status": 404, "error": "Not Found", "message": "User not found"}

    update_password_hashed = bcrypt.hashpw(
        update_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Store old values before change
    old_user_name = user_query.user_name
    old_first_name = user_query.first_name
    old_last_name = user_query.last_name
    old_password = user_query.password
    old_email = user_query.email
    old_role = user_query.role

    user_query.user_name = update_username
    user_query.first_name = update_first_name
    user_query.last_name = update_last_name
    user_query.password = update_password_hashed
    user_query.email = update_email
    user_query.role = update_role
    user_query.updated_at = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    try:
        save_user_log_service(
            {
                "user_id": id,
                "log_type": "update",
                "log_details": {
                    "user_id": update_user_id,
                    "changes": {
                        "username": {"old": old_user_name, "new": update_username},
                        "first_name": {"old": old_first_name, "new": update_first_name},
                        "last_name": {"old": old_last_name, "new": update_last_name},
                        "password": {
                            "old": old_password,
                            "new": update_password_hashed,
                        },
                        "email": {"old": old_email, "new": update_email},
                        "role": {"old": old_role, "new": update_role},
                    },
                },
            }
        )
    except Exception as e:
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    return {
        "message": "User updated successfully",
        "data": {
            "user_id": {
                "old": update_user_id,
                "new": user_query.user_id,
            },
            "username": {
                "old": old_user_name,
                "new": update_username,
            },
            "first_name": {
                "old": old_first_name,
                "new": update_first_name,
            },
            "last_name": {
                "old": old_last_name,
                "new": update_last_name,
            },
            "email": {
                "old": old_email,
                "new": update_email,
            },
            "role": {
                "old": old_role,
                "new": update_role,
            },
        },
    }


def delete_user_service(args, id):
    delete_user_id = args.get("user_id")

    if not delete_user_id:
        return (
            {"status": 400, "error": "Bad Request", "message": "User ID is required"},
        )

    user_query = User.query.filter_by(user_id=delete_user_id).first()

    if not user_query:
        return ({"status": 404, "error": "Not Found", "message": "User not found"},)

    # Store values before deletion
    old_user_name = user_query.user_name
    old_first_name = user_query.first_name
    old_last_name = user_query.last_name
    old_email = user_query.email
    old_role = user_query.role
    old_user_id = user_query.user_id

    try:
        db.session.delete(user_query)
        db.session.commit()
    except Exception as e:
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    try:
        save_user_log_service(
            {
                "user_id": id,
                "log_type": "delete",
                "log_details": {
                    "user_id": old_user_id,
                    "user_name": old_user_name,
                    "first_name": old_first_name,
                    "last_name": old_last_name,
                    "email": old_email,
                    "role": old_role,
                },
            }
        )
    except Exception as e:
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    return {
        "message": "User deleted successfully",
        "data": {
            "user_id": old_user_id,
            "username": old_user_name,
            "first_name": old_first_name,
            "last_name": old_last_name,
            "email": old_email,
            "role": old_role,
        },
    }


def create_user_service(args, id):
    create_username = args.get("username")
    create_first_name = args.get("first_name")
    create_last_name = args.get("last_name")
    create_password = args.get("password")
    create_confirm_password = args.get("confirm_password")
    create_email = args.get("email")
    create_role = args.get("role")

    if not all(
        [
            create_username,
            create_first_name,
            create_last_name,
            create_password,
            create_confirm_password,
            create_email,
            create_role,
        ]
    ):
        return {
            "status": 400,
            "error": "Bad Request",
            "message": "All fields are required",
        }

    if create_password != create_confirm_password:
        return {
            "status": 400,
            "error": "Bad Request",
            "message": "Passwords do not match",
        }

    users = User.query.filter_by(user_name=create_username).all()

    for user in users:
        # Check if the username and email already exists
        if user.user_name == create_username or user.email == create_email:
            # Check if the password matches the existing user's password
            if bcrypt.checkpw(
                create_password.encode("utf-8"), user.password.encode("utf-8")
            ):
                return {
                    "status": 400,
                    "error": "Bad Request",
                    "message": "Username or email already exists",
                }

    new_user_id = str(uuid4()) if args.get("user_id") is None else args.get("user_id")

    user = User(
        user_name=create_username,
        first_name=create_first_name,
        last_name=create_last_name,
        password=bcrypt.hashpw(
            create_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        email=create_email,
        role=create_role,
        user_id=new_user_id,
        start_date=datetime.now(),
        updated_at=datetime.now(),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return {"status": 500, "message": str(e)}

    try:
        save_user_log_service(
            {
                "user_id": id,
                "log_type": "create",
                "log_details": {
                    "user_id": new_user_id,
                    "user_name": create_username,
                    "first_name": create_first_name,
                    "last_name": create_last_name,
                    "email": create_email,
                    "role": create_role,
                },
            }
        )
    except Exception as e:
        return {"status": 500, "message": str(e)}

    return {
        "message": "User created successfully",
        "data": {
            "user_id": new_user_id,
            "username": create_username,
            "first_name": create_first_name,
            "last_name": create_last_name,
            "email": create_email,
            "role": create_role,
        },
    }


def get_all_users_service(id):

    users = User.query.all()

    try:
        save_user_log_service(
            {
                "user_id": id,
                "log_type": "get_all_users",
                "log_details": {
                    "user_id": [user.user_id for user in users],
                },
            }
        )
    except Exception as e:
        return {"status": 500, "message": str(e)}

    return [
        {
            "username": user.user_name,
            "email": user.email,
            "role": user.role,
            "user_id": user.user_id,
        }
        for user in users
    ]


def save_user_log_service(args):

    user_log = UserLogs(
        user_id=args.get("user_id"),
        log_id=str(uuid4()),
        log_date=datetime.now(),
        log_type=args.get("log_type"),
        log_details=json.dumps(args.get("log_details")),
    )
    try:
        db.session.add(user_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"status": 500, "message": str(e)}


def clerk_user_service(payload, event_type):
    """
    Handle POST request from clerk user authentication webhook.
    This includes following events:
        email.created
        session.created
        session.ended
        session.pending
        session.removed
        session.revoked
        user.created
        user.deleted
        user.updated
    """
    # user_id = payload.get("data").get("user_id")
    # status = payload.get("data").get("status")
    # expire_at = payload.get("data").get("expire_at")
    # created_at = payload.get("data").get("created_at")
    # ecent_type = event_type
    pass
