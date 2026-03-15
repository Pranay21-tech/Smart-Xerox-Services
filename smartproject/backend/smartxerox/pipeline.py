def save_user_email(strategy, details, user=None, *args, **kwargs):
    if user:
        request = strategy.request

        # Django default user email field
        email = user.email

        if email:
            request.session["user_email"] = email