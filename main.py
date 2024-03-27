from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def first_page():
    return render_template("first_page.html")


@app.route("/recipes")
def second_page():
    return render_template("second_page.html")

