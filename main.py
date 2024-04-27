from flask import Flask, render_template, request
from data.users import User
from data.recipes import Recipe
from data.comments import Comment
from data import db_session
import os
import datetime


MAIN_USER = ""
UPLOAD_FOLDER = "static/data/image"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_comments(recipeid):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    comments = [
        comment
        for comment in db_sess.query(Comment)
        .filter(Comment.recipeid == recipeid, Comment.status == "Активен")
        .all()
    ]
    comments = [
        [
            db_sess.query(User).filter(User.id == comment.userid).first().name,
            comment.content,
        ]
        for comment in comments
    ]
    return comments


def get_main_users_recipes():
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    userid = (
        db_sess.query(User)
        .filter(User.name == MAIN_USER, User.status == "Активен")
        .first()
        .id
    )
    recipes = [
        recipe
        for recipe in db_sess.query(Recipe)
        .filter(Recipe.userid == userid, Recipe.status == "Активен")
        .all()
    ]
    recipes = [
        [
            i + 2,
            db_sess.query(User).filter(User.id == recipe.userid).first().name,
            recipe.name,
            f"{recipe.category.capitalize(  )}: {recipe.description[:]}"[:],
            recipe.path_to_photo.replace("\\", "/"),
            recipe.id,
        ]
        for i, recipe in enumerate(recipes)
    ]
    return recipes


def sorted_recipes(condition):
    CONDITION = {"По дате создания": 0, "По автору": 1, "По алфавиту": 2}
    main_condition = CONDITION[condition]

    recipes = get_recipes()
    return sorted(recipes, key=lambda x: x[main_condition])


def filter_recipes(condition):
    recipes = get_recipes()
    recipes = list(
        filter(lambda x: x[3].split(": ")[0] == condition.capitalize(), recipes)
    )
    recipes = [
        [i + 1, recipe[1], recipe[2], recipe[3], recipe[4], recipe[5]]
        for i, recipe in enumerate(recipes)
    ]
    return recipes


def get_recipes():
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    recipes = [
        recipe
        for recipe in db_sess.query(Recipe).filter(Recipe.status == "Активен").all()
    ]
    recipes = [
        [
            i + 1,
            db_sess.query(User).filter(User.id == recipe.userid).first().name,
            recipe.name,
            f"{recipe.category.capitalize(  )}: {recipe.description[:]}"[:],
            recipe.path_to_photo.replace("\\", "/"),
            recipe.id,
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


def add_comment(comment, recipe_id):
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()

    new_comment = Comment()
    new_comment.userid = db_sess.query(User).filter(User.name == MAIN_USER).first().id
    new_comment.recipeid = recipe_id
    new_comment.content = comment
    new_comment.status = "Активен"

    db_sess.add(new_comment)
    db_sess.commit()


def add_recipe(recipe):
    global MAIN_USER
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()

    new_recipe = Recipe()
    new_recipe.userid = db_sess.query(User).filter(User.name == MAIN_USER).first().id
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


def delete_recipe(id):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    recipe = (
        db_sess.query(Recipe)
        .filter(Recipe.id == id and Recipe.status == "Активен")
        .first()
    )
    recipe.status = "Удален"
    recipe.changed_date = datetime.datetime.now()
    db_sess.commit()
    return profile_user()


def correct_password(name, password):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).filter(User.name == name):
        return user.password == password


def get_about_recipe(id_recipe):
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    recipe = (
        db_sess.query(Recipe)
        .filter(Recipe.status == "Активен", Recipe.id == id_recipe)
        .first()
    )
    recipe = [
        recipe.id,
        db_sess.query(User).filter(User.id == recipe.userid).first().name,
        recipe.name,
        f"{recipe.category.capitalize(  )}: {recipe.description[:]}"[:],
        recipe.path_to_photo.replace("\\", "/"),
        recipe.id,
    ]

    return recipe


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
        path = os.path.join(app.config["UPLOAD_FOLDER"], recipe_image.filename)
        recipe_image.save(path.replace("\\", "/"))
        add_recipe(
            [
                recipe_title,
                recipe_description,
                recipe_category,
                path[7:],
            ]
        )
        return render_template("profile_page.html", user=get_data_user())


@app.route("/recipes", methods=["GET", "POST"])
def recipes_page():
    global MAIN_USER
    if request.method == "POST" and request.form["recipe_category"] != "Все":
        condition = request.form["recipe_category"]
        recipes = filter_recipes(condition)
        return render_template(
            "recipes_page.html", recipes=recipes, main_user=MAIN_USER
        )
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


@app.route("/profile", methods=["POST", "GET"])
def profile_user():
    global MAIN_USER
    data_user = get_data_user()
    recipes = get_main_users_recipes()
    return render_template("profile_page.html", user=data_user, recipes=recipes)


@app.route("/about_recipe", methods=["POST", "GET"])
def about_recipes():
    global MAIN_USER
    if "submit" in request.form:
        id_recipe = request.form["submit"]
    if "comment" in request.form and MAIN_USER:
        content = request.form["comment"]
        add_comment(content, id_recipe)
    elif "get_recipe" in request.form:
        id_recipe = request.form["get_recipe"]
    recipe = get_about_recipe(id_recipe)
    comments = get_comments(id_recipe)
    return render_template(
        "about_recipe.html", recipe=recipe, main_user=MAIN_USER, comments=comments
    )


@app.route("/delete_recipe", methods=["POST", "GET"])
def delete_recipe_users():
    id_recipe = request.form["get_recipe"]
    return delete_recipe(id_recipe)
