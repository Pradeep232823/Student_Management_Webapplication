import re

def is_valid_name(name):

    if not name:
        return False, "Name is required"

    if not name.replace(" ","").isalpha():
        return False, "Name should contain only alphabets"

    if len(name) < 2 or len(name) > 100:
        return False, "Name length must lie between 2 to 100"
    
    return True, name

def is_valid_department(department):
    if not department:
        return False, "Department is required"

    if not department.replace(" ","").isalpha():
        return False, "Department should contain only alphabets"

    if len(department) < 2 or len(department) > 100:
        return False, "Department length must lie between 2 to 100"
    
    return True, department

def is_valid_email(email):
    regex_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
    if not re.fullmatch(regex_pattern, email):
        return False, "Email pattern is invalid"
    
    if len(email) < 5 or len(email) > 150:
        return False, "Email length is invalid"

    return True, email

def validate_student_data(name, department, email):
    isvalid_name, name = is_valid_name(name)
    
    if not isvalid_name:
        return False, name

    isvalid_department, department = is_valid_department(department)

    if not isvalid_department:
        return False, department

    isvalid_email, email = is_valid_email(email)

    if not isvalid_email:
        return False, email

    return True, (name, department, email)



def is_valid_username(username):

    if not username:
        return False, "Username is required"

    if len(username) < 3 or len(username) > 50:
        return False, "Username length must lie between 3 to 50"

    if not re.fullmatch(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can contain only letters, numbers and underscore"

    return True, username

def is_valid_password(password):

    if not password:
        return False, "Password is required"

    if len(password) < 8 or len(password) > 128:
        return False, "Password length must lie between 8 to 128"

    return True, password

def validate_login_data(username, password):

    if not username:
        return False, "Username is required"

    if not password:
        return False, "Password is required"

    return True, (username, password)