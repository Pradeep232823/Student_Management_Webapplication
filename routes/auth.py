from flask import render_template, Blueprint, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import create_user, get_user, get_dashboard_data
from utils.auth_utils import login_required
from utils.validators import is_valid_username, is_valid_password, is_valid_email, validate_login_data


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login_page():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form["username"].strip()
    password = request.form["password"]

    is_valid, result = validate_login_data(username, password)

    if not is_valid:
        flash(result, "error")
        return redirect("/login")

    username, password = result

    user = get_user(username)

    if user is None:
        flash("Invalid username or password.", "error")
        return redirect("/login")

    user_id = user[0]
    stored_hash = user[3]

    if not check_password_hash(stored_hash, password):
        flash("Invalid username or password.", "error")
        return redirect("/login")

    session["user_id"] = user_id
    session["username"] = user[1]

    # print("Login successful")
    # print("User ID:", user_id)
    # print("Username:", user[1])

    flash("Login Successful", "success")
    return redirect("/dashboard")


@auth_bp.route("/register")
def register_page():

    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register():

    username = request.form["username"].strip()
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    is_valid, result = is_valid_username(username)

    if not is_valid:
        flash(result, "error")
        return redirect("/register")


    is_valid, result = is_valid_email(email)

    if not is_valid:
        flash(result, "error")
        return redirect("/register")


    is_valid, result = is_valid_password(password)

    if not is_valid:
        flash(result, "error")
        return redirect("/register")


    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect("/register")

    hashed_password = generate_password_hash(password)

    is_created, result = create_user(
        username=username,
        email=email,
        password=hashed_password
    )

    if is_created is False:
        flash(result, "error")
        return redirect("/register")

    if is_created is None:
        flash("Something went wrong!", "error")
        return redirect("/register")

    flash("User registered successfully.", "success")

    return redirect("/login")


@auth_bp.route("/dashboard")
@login_required
def dashboard():

    username = session.get("username")

    dashboard_data = get_dashboard_data()

    if dashboard_data is None:
        flash("Something went wrong", "error")
        return redirect("/")

    dashboard_data["username"] = username

    return render_template("dashboard.html", dashboard_data = dashboard_data)


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect("/")