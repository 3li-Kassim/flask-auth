from flask import Flask
from extensions import db,bcrypt
from routes import auth

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SECRET_KEY"] = "supersecretkey"

app.register_blueprint(auth)

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug = True)