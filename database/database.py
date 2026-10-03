import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DATABASE
from mysql.connector import IntegrityError
from datetime import datetime

def get_db_connection():

    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port = MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    return connection

def get_all_students(search=""):
    
    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None: 
            return None

        query = "SELECT id, name, department, email FROM students WHERE name LIKE %s OR department LIKE %s OR email LIKE %s"

        search_value = f"%{search}%"

        cursor.execute(query, (search_value, search_value, search_value))

        return cursor.fetchall()

    except Exception as e:
        print(e)
        return None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)


def create_student(name, department, email):
    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None: 
            return None, None

        query = "INSERT INTO students(name, department, email) values(%s, %s, %s);"
        
        values = (name, department, email)

        cursor.execute(query, values)

        conn.commit()

        print("Student inserted successfully")

        return True, None
    
    except IntegrityError as e:
        if conn:
            conn.rollback()

        print(e)
        return False, email
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None, None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)


def get_edit_student(std_id):
    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None: 
            return None, None

        query = "SELECT id, name, department, email FROM students WHERE id = %s"
        cursor.execute(query, (std_id,))

        student = cursor.fetchone()

        if not student:
            return False
        return student

    except Exception as e:
        print(e)
        return None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)


def update_student_data(id, name, department, email):
    conn, cursor = None, None
    
    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None: 
            return None, None

        query = "SELECT id, name, department, email FROM students WHERE id = %s"
        cursor.execute(query, (id,))
        if not cursor.fetchone():
            return False, False

        query = "UPDATE students SET name = %s, department = %s, email = %s where id = %s"
        values = (name, department, email, id)

        cursor.execute(query,values)
        conn.commit()

        return True, None

    except IntegrityError as e:
        if conn:
            conn.rollback()

        print(e)
        return False, email

    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None, None
    
    finally:
        close_cursor_conn(cursor=cursor, conn=conn)


def delete_student_data(id):
    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None:
            return None, None

        query = "DELETE FROM students WHERE id = %s"
        cursor.execute(query, (id,))

        rowcount = cursor.rowcount
        # print(f"Row count at deletion process: {rowcount}")

        conn.commit()

        if rowcount == 0:
            return False, None        
        
        return True, None

    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None, None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)

def create_user(username, email, password):

    conn, cursor = None, None

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None:
            return None, None

        query = "INSERT INTO users (username, email, password, created_at) VALUES (%s, %s, %s, %s)"

        values = (username, email, password, created_at)

        cursor.execute(query, values)
        conn.commit()

        print("User created successfully")
        return True, None

    except IntegrityError as e:
        if conn:
            conn.rollback()
        print(e)
        return False, "Username or email already exists."

    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None, None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)


def get_user(username):

    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        if conn is None or cursor is None:
            return None

        query = """
            SELECT id, username, email, password
            FROM users
            WHERE username = %s
        """

        cursor.execute(query, (username,))

        user = cursor.fetchone()

        if not user:
            return None

        return user

    except Exception as e:

        if conn:
            conn.rollback()

        print(e)

        return None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)

def get_dashboard_data():
    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT department) FROM students")
        total_departments = cursor.fetchone()[0]

        cursor.execute("SELECT department, COUNT(department) FROM students GROUP BY department")
        students_by_department = cursor.fetchall()

        if total_students is None or total_departments is None or students_by_department is None:
            return None

        dashboard_data = {
            "total_students":total_students, 
            "total_departments":total_departments, 
            "students_by_departments":students_by_department
        }

        return dashboard_data

    except Exception as e:
        print(e)
        return None

    finally:
        close_cursor_conn(cursor=cursor, conn=conn)

def get_conn_cursor():
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        return conn, cursor

    except Exception as e:
        print(e)
        return None, None

def close_cursor_conn(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()