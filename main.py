from flask import Flask, render_template, request
from data.users import User
from data.recipes import Recipe
from data.comments import Comment
from data import db_session

app = Flask(__name__)


def get_recipes():
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    recipes = [recipe for recipe in db_sess.query(Recipe).all()]
    recipes = [
        [i, "Я", recipe.name, recipe.description] for i, recipe in enumerate(recipes)
    ]
    return recipes


def is_registered(name, email):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    if [x for x in db_sess.query(User).filter(User.name == name)] or [
        x for x in db_sess.query(User).filter(User.email == email)
    ]:
        return True
    return False


def is_login(name):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.name == name)


def correct_password(name, password):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).filter(User.name == name):
        return user.password == password


@app.route("/")
def first_page():
    return render_template("first_page.html")


@app.route("/recipes")
def recipes_page():
    recipes = get_recipes()
    return render_template("recipes_page.html", recipes=recipes)


@app.route("/registration", methods=["POST", "GET"])
def registration_user():
    if request.method == "GET":
        return render_template("registration_page.html")

    elif request.method == "POST":
        if not is_registered(request.form["name"], request.form["email"]):
            db_session.global_init("CookingMyself.db")
            db_sess = db_session.create_session()

            user = User()
            user.name = request.form["name"]
            user.email = request.form["email"]
            user.password = request.form["password"]
            user.status = "Активен"
            db_sess.add(user)

            db_sess.commit()
            return render_template("first_page.html")

        return render_template("login_page.html")


@app.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == "GET":
        return render_template("login_page.html")

    elif request.method == "POST":
        if not is_login(request.form["name"]):
            return render_template("registration_page.html")

        if not correct_password(request.form["name"], request.form["password"]):
            return render_template("login_page.html")

        return render_template("first_page.html")
