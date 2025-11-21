import json
import bcrypt
from flask_jwt_extended import create_access_token
from auth.user_model import User, UserLogs
from uuid import uuid4
from datetime import datetime, timedelta
from db.database import db
from flask import session
from configs.paths import *
# from configs.paths_local import *


def login_user_service(args):

    login_username = args.get("username")
    login_email = args.get("email")
    login_password = args.get("password")

    if login_username:
        user_query = User.query.filter_by(user_name=login_username, user_id=login_password).first()
    else:
        user_query = User.query.filter_by(email=login_email, user_id=login_password).first()

    if not user_query or not bcrypt.checkpw(
        login_password.encode("utf-8"), user_query.password.encode("utf-8")
    ):    
        return (
            {
                "status": 401,
                "error": "Unauthorized",
                "message": "Invalid credentials",
            },
        )
    else:
        user_query.last_login = datetime.now()

        # Store values before commit
        user_id = user_query.user_id
        user_name = user_query.user_name
        user_first_name = user_query.first_name
        user_last_name = user_query.last_name
        user_email = user_query.email
        role = get_user_role(user_query)

        db.session.commit()

        try:
            save_user_log_service(
                {
                    "user_id": user_id,
                    "log_type": "login",
                    "log_details": {
                        "event": "login",
                        "source": "auth_service.login_user_service",
                        "user": {
                            "user_id": user_id,
                            "user_name": user_name,
                            "first_name": user_first_name,
                            "last_name": user_last_name,
                            "role": role,
                            "email": user_email,
                        },
                        "message": "Login successful",
                        "context": {},
                    },
                }
            )
            access_token = create_access_token(
                identity= user_id,
                additional_claims={
                    "user_name": user_name,
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "role": role,
                    "user_id": user_id,
                    "email_address": user_email,
                },
                expires_delta=timedelta(hours=1),
            )
        except Exception as e:
            db.session.rollback()
            return {"status": 500, "error": "Internal Server Error", "message": str(e)}

        return {
            "message": "Login successful",
            "data": {
                "user_id": user_id,
                "user_name": user_name,
                "first_name": user_first_name,
                "last_name": user_last_name,
                "email_address": user_email,
                "role": role,
            },
            "token": access_token,
            "status": 200,
        }


def logout_user_service(args):
    """
    This function logs out the user if the user is logged in
    """
    try:
        save_user_log_service(
            {
                "user_id": args.get("user_id"),
                "log_type": "logout",
                "log_details": {
                    "event": "logout",
                    "source": "auth_service.logout_user_service",
                    "user": {
                        "user_id": args.get("user_id"),
                    },
                    "message": "Logout successful",
                    "context": {},
                },
            }
        )
        session.clear()
    except Exception as e:
        db.session.rollback()
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    return {"status": 200, "message": "Logout successful"}


def get_user_role(user_query):
    if user_query:
        return user_query.role if hasattr(user_query, "role") else "guest"
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

    # Check if the user has permission to update
    authenticated_user = get_user_by_id_service(id)
    
    if authenticated_user.role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {authenticated_user.user_id} and role {authenticated_user.role} is not authorized to access this resource.",
        }

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
                    "event": "update",
                    "source": "auth_service.update_user_service",
                    "user": {
                        "user_id": update_user_id,
                        "user_name": update_username,
                        "first_name": update_first_name,
                        "last_name": update_last_name,
                        "email": update_email,
                        "role": update_role,
                    },
                    "message": "User updated",
                    "context": {
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
                        }
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


def delete_user_service(id, current_user):

    if not id:
        return (
            {"status": 400, "error": "Bad Request", "message": "User ID is required"},
        )

    authenticated_user = get_user_by_id_service(current_user)

    if authenticated_user.role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {authenticated_user.user_id} and role {authenticated_user.role} is not authorized to access this resource.",
        }

    user_query = User.query.filter_by(user_id=id).first()

    if not user_query:
        return ({"status": 404, "error": "Not Found", "message": "User not found"},)

    # Store values before deletion
    deleted_user_name = user_query.user_name
    deleted_first_name = user_query.first_name
    deleted_last_name = user_query.last_name
    deleted_email = user_query.email
    deleted_role = user_query.role
    deleted_user_id = user_query.user_id

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
                    "event": "delete",
                    "source": "auth_service.delete_user_service",
                    "user": {
                        "user_id": deleted_user_id,
                        "user_name": deleted_user_name,
                        "first_name": deleted_first_name,
                        "last_name": deleted_last_name,
                        "email": deleted_email,
                        "role": deleted_role,
                    },
                    "message": "User deleted",
                    "context": {},
                },
            }
        )
    except Exception as e:
        return {"status": 500, "error": "Internal Server Error", "message": str(e)}

    return {
        "message": "User deleted successfully",
        "data": {
            "user_id": deleted_user_id,
            "username": deleted_user_name,
            "first_name": deleted_first_name,
            "last_name": deleted_last_name,
            "email": deleted_email,
            "role": deleted_role,
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
                    "event": "create",
                    "source": "auth_service.create_user_service",
                    "user": {
                        "user_id": new_user_id,
                        "user_name": create_username,
                        "first_name": create_first_name,
                        "last_name": create_last_name,
                        "email": create_email,
                        "role": create_role,
                    },
                    "message": "User created",
                    "context": {},
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

    try:
        user = get_user_by_id_service(id)
    except Exception as e:
        return {"status": 500, "message": str(e)}

    if not user:
        return {"status": 404, "message": "User not found"}

    if user.role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user.user_id} and role {user.role} is not authorized to access this resource.",
        }

    users = User.query.all()

    try:
        save_user_log_service(
            {
                "user_id": id,
                "log_type": "get_all_users",
                "log_details": {
                    "event": "get_all_users",
                    "source": "auth_service.get_all_users_service",
                    "user": {
                        "user_id": id,
                        "role": user.role,
                    },
                    "message": "Fetched all users",
                    "context": {"count": len(users), "user_ids": [u.user_id for u in users]},
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


def get_user_by_id_service(id):
    """
    Get a user by their id.

    Args:
        id (int): The id of the user.

    Returns:
        User: The user object if found, None otherwise.
    """
    user = User.query.filter(User.user_id == id).order_by(User.start_date.desc()).first()

    return user


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


def update_last_login_service(user_id: str):
    """Update the last_login field for the given user_id."""
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"status": 404, "message": "User not found"}
        user.last_login = datetime.now()
        db.session.commit()
        # Optional: log this change
        save_user_log_service(
            {
                "user_id": user_id,
                "log_type": "login_last_login_update",
                "log_details": {
                    "event": "update_last_login",
                    "source": "auth_service.update_last_login_service",
                    "user": {"user_id": user_id},
                    "message": "last_login timestamp updated",
                    "context": {},
                },
            }
        )
        return {"status": 200, "message": "last_login updated"}
    except Exception as e:
        db.session.rollback()
        return {"status": 500, "message": str(e)}
