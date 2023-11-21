from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy
import os

app = Flask(__name__)

"""db = SQLAlchemy("sqlite:///db.sqlite")"""

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Message(db.Model): #message je ime tablice
    id = db.Column(db.Integer, primary_key=True) #id, author, text - imena stupaca
    author = db.Column(db.String, unique=False) #Column = stupac
    text = db.Column(db.String, unique=False)

db.create_all()

"""@app.route("/")
def index():
    return render_template("index.html")"""


@app.route("/", methods=["GET"])
def index():
    messages = db.query(Message).all()

    return render_template("index.html", messages=messages)


@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    """print("{0}: {1}".format(username, text))"""

    message = Message(author=username, text=text) #autora pročitali iz username, text iz texta u formularu
    message.save() #spremi u bazu, inače ostane u nekoj varijabli

    return redirect("/")


if __name__ == '__main__':
    app.run()
