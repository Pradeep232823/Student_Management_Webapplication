from flask import Flask

from routes.main import main_bp
from routes.students import students_bp
from routes.auth import auth_bp

from config import APP_SECRET_KEY

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.secret_key = APP_SECRET_KEY

csrf = CSRFProtect(app)

app.register_blueprint(main_bp)
app.register_blueprint(students_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True)