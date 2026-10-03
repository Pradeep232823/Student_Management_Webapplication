from functools import wraps
from flask import session, redirect, flash


def login_required(view_function):

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login to continue.", "error")
            return redirect("/login")

        return view_function(*args, **kwargs)

    return wrapper