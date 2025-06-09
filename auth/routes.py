from auth.auth_controller import user_controller, user_create_controller


def authentication_routes(api):
    """
    Registers authentication-related routes with the provided API instance.

    Args:
        api: The API instance to which the authentication routes will be added.
    """

    # Login route for JWT authentication
    api.add_resource(
        user_controller, "/auth/login", endpoint="auth_login", methods=["POST"]
    )
    # Create route for user creation
    api.add_resource(
        user_create_controller, "/auth/create", endpoint="auth_create", methods=["POST"]
    )
    # Delete route for user deletion
    api.add_resource(
        user_controller, "/auth/delete", endpoint="auth_delete", methods=["DELETE"]
    )
    # Update route for user update
    api.add_resource(
        user_controller, "/auth/update", endpoint="auth_update", methods=["PUT"]
    )
    # Get all users route
    api.add_resource(
        user_controller, "/auth/users", endpoint="auth_users", methods=["GET"]
    )
