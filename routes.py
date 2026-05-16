from extensions import db,bcrypt
from flask import Blueprint,render_template,request,redirect,url_for,session
from models import User
from functools import wraps

auth = Blueprint("auth", __name__)



@auth.route("/register", methods=["GET","POST"])
def register():
   if request.method == "POST":
       username = request.form["username"]
       email = request.form["email"]
       password =request.form["password"]
       password = bcrypt.generate_password_hash(password)
       user = User(username = username, email= email, password = password)
       db.session.add(user)
       db.session.commit()
       return redirect("/login") 
   return render_template("register.html") 

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email = email).first()
        if user:
            password = request.form["password"]
            if bcrypt.check_password_hash(user.password,password):
                session["user_id"] = user.id
                return redirect("/dashboard")
            else:
                return redirect("/login")
        else:
            return redirect("/login")
    return render_template("login.html")


def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return func(*args,**kwargs)
    return wrapper

@auth.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html",user= user)   

@auth.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/login")   

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.query.get(session["user_id"])
        if user.role != "admin":
            return redirect("/dashboard")
        return func(*args,**kwargs)
    return wrapper

@auth.route("/admin", methods=["GET"])
@login_required
@admin_required
def admin_login():
    user = User.query.get(session["user_id"])
    all_users = User.query.all()
    return render_template("admin.html",user=user,users = all_users)
            