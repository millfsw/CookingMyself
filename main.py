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
            recipe.description[:],
            recipe.path_to_photo.replace("\\", "/"),
        ]
        for i, recipe in enumerate(recipes)
    ]
    return recipes


def get_data_user():
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    data_user = (
        db_sess.query(User)
        .filter(User.name == MAIN_USER, User.status == "Активен")
        .first()
    )

    return data_user.name, data_user.email


def add_recipe(recipe):
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()

    new_recipe = Recipe()
    new_recipe.userid = db_sess.query(User).filter(User.name == MAIN_USER).userid
    new_recipe.name = recipe[0]
    new_recipe.description = recipe[1]
    new_recipe.category = recipe[2]
    new_recipe.path_to_photo = recipe[3]
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
    global MAIN_USER
    return render_template("first_page.html", main_user=MAIN_USER)


@app.route("/logout")
def logout():
    global MAIN_USER
    MAIN_USER = ""
    return render_template("first_page.html", main_user=MAIN_USER)


@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    if request.method == "GET":
        return render_template("create_recipe_page.html")

    elif request.method == "POST":
        recipe_title = request.form["recipe-title"]
        recipe_description = request.form["recipe-description"]
        recipe_category = request.form["recipe-category"]
        recipe_image = request.files["recipe-image"]
        add_recipe([recipe_title, recipe_description, recipe_category, recipe_image])
        return render_template("profile_page.html")


@app.route("/recipes")
def recipes_page():
    global MAIN_USER
    recipes = get_recipes()
    return render_template("recipes_page.html", recipes=recipes, main_user=MAIN_USER)


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
            return render_template("first_page.html", main_user=MAIN_USER)

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
            return render_template("login_page.html")

        MAIN_USER = request.form["name"]
        return render_template("first_page.html", main_user=MAIN_USER)


@app.route("/profile")
def profile_user():
    global MAIN_USER
    data_user = get_data_user()
    return render_template("profile_page.html", user=data_user)
