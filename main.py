from flask import Flask, render_template, request
from data.users import User
from data.recipes import Recipe
from data.comments import Comment
from data import db_session

app = Flask(__name__)
MAIN_USER = ""


def get_recipes():
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    recipes = [recipe for recipe in db_sess.query(Recipe).all()]
    recipes = [
        [
            i + 1,
            db_sess.query(User).filter(User.id == recipe.userid).first().name,
            recipe.name,
            recipe.description[:220],
            recipe.path_to_photo,
        ]
        for i, recipe in enumerate(recipes)
    ]
    return recipes


def add_recipe(recipe):
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()

    new_recipe = Recipe()
    new_recipe.userid = db_sess.query(User).filter(User.name == MAIN_USER).userid
    new_recipe.name = recipe[1]
    new_recipe.description = recipe[2]
    new_recipe.category = recipe[3]
    new_recipe.path_to_photo = recipe[4]
    new_recipe.status = "Активен"

    db_sess.add(new_recipe)
    db_sess.commit()


def add_user(user):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()

    new_user = User()
    new_user.name = user[0]
    new_user.email = user[1]
    new_user.password = user[2]
    new_user.status = "Активен"
    db_sess.add(new_user)

    db_sess.commit()


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
    global MAIN_USER
    if request.method == "GET":
        return render_template("registration_page.html")

    elif request.method == "POST":
        if not is_registered(request.form["name"], request.form["email"]):
            add_user(
                [request.form["name"], request.form["email"], request.form["password"]]
            )
            MAIN_USER = request.form["name"]
            return render_template("first_page.html")

        return render_template("login_page.html")


@app.route("/login", methods=["POST", "GET"])
def login_user():
    global MAIN_USER
    if request.method == "GET":
        return render_template("login_page.html")

    elif request.method == "POST":
        if not is_login(request.form["name"]):
            return render_template("registration_page.html")

        if not correct_password(request.form["name"], request.form["password"]):
            MAIN_USER = request.form["name"]
            return render_template("login_page.html")

        return render_template("first_page.html")
