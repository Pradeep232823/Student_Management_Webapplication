from flask import render_template, request, redirect, Blueprint, flash, jsonify

from database.database import get_all_students, create_student, update_student_data, delete_student_data, get_edit_student
from utils.validators import validate_student_data
from utils.auth_utils import login_required

students_bp = Blueprint("students",__name__)

@students_bp.route("/students")
@login_required
def students():

    search = request.args.get("search", "")

    students = get_all_students(search=search)

    if students is None:
        flash("Something went wrong!", "error")
        return redirect("/students")

    students_data = []

    for student in students:

        students_data.append({
            "id": student[0],
            "name": student[1],
            "department": student[2],
            "email": student[3]
        })
    
    return render_template("students.html", students=students_data)


@students_bp.route("/api/students")
@login_required
def get_students_api():

    students = get_all_students()

    if students is None:
        return jsonify({
            "error": "Something went wrong!"
        }), 500

    students_data = []

    for student in students:

        students_data.append({
            "id": student[0],
            "name": student[1],
            "department": student[2],
            "email": student[3]
        })

    return jsonify(students_data)


@students_bp.route("/students/add")
@login_required
def add_student_page():
    return render_template("add_student.html")


@students_bp.route("/students/add", methods=["POST"])
@login_required
def add_student():
    
    name = request.form["name"].strip()
    department = request.form["department"].strip()
    email = request.form["email"].strip().lower()

    is_valid_data, result = validate_student_data(name=name, department=department, email=email)

    if not is_valid_data:
        flash(result, "error")
        return redirect("/students/add")

    name, department, email = result
    
    is_created, result = create_student(name=name, department=department, email=email)

    if not is_created and result == email:
        flash("Email already exists. Try another.", "error")
        return redirect("/students/add")
    
    elif is_created is None and result is None:
        flash("Something went wrong!", "error")
        return redirect("/students/add")

    flash("Student added successfully", "success")
    return redirect("/students")

@students_bp.route("/students/edit/<int:id>")
@login_required
def edit_student(id):

    student = get_edit_student(std_id=id)

    if student is False:
        flash("Student not found", "error")
        return redirect("/students")

    if student is None:
        flash("Something went wrong!", "error")
        return redirect("/students")

    student_data = {
        "id": student[0],
        "name": student[1],
        "department": student[2],
        "email": student[3]
    }

    return render_template("edit_student.html", student=student_data)

@students_bp.route("/students/edit/<int:id>", methods = ["POST"])
@login_required
def update_student(id):

    name = request.form["name"].strip()
    department = request.form["department"].strip()
    email = request.form["email"].strip().lower()

    is_valid_data, result = validate_student_data(name=name, department=department, email=email)

    if not is_valid_data:
        flash(result, "error")
        return redirect(f"/students/edit/{id}")

    name, department, email = result

    is_updated, result = update_student_data(id=id, name=name, department=department, email=email)

    if not is_updated and result == email:
        flash("Email already exists. Try another.", "error")
        return redirect(f"/students/edit/{id}")

    if is_updated is False and result is False:
        flash("Student does not exist", "error")
        return redirect(f"/students/edit/{id}")

    if is_updated is None and result is None:
        flash("Something went wrong!", "error")
        return redirect(f"/students/edit/{id}")

    flash("Student updated successfully", "success")
    return redirect("/students")

@students_bp.route("/students/delete/<int:id>", methods=["POST"])
@login_required
def delete_student(id):

    is_deleted, result = delete_student_data(id=id)

    if is_deleted is False and result is None:
        flash("Student does not exist", "error")
        return redirect("/students")

    if is_deleted is None and result is None:
        flash("Something went wrong!", "error")
        return redirect("/students")

    flash("Student deleted successfully", "success")
    return redirect("/students")