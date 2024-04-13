from flask import Flask, render_template
from CookingMyself.data.users import User
from CookingMyself.data import db_session

app = Flask(__name__)


@app.route("/")
def first_page():
    return render_template("first_page.html")


@app.route("/recipes")
def second_page():
    recipes = get_recipes()
    return render_template("second_page.html", recipes=recipes)


def get_recipes():
    db_session.global_init("CookingMyself.db")
    db_sess = db_session.create_session()
    return [recipe for recipe in db_sess.query(Recipe).all()]


@app.route("/registration")
def registration_user():
    if request.method == "GET":
        return render_template("registration_page.html")

    elif request.method == "POST":
        db_session.global_init("CookingMyself.db")
        db_sess = db_session.create_session()

        user = User()
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.password = request.form["password"]
        user.status = "Активен"
        db_sess.add(user)

        db_sess.commit()
