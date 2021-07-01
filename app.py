import os
import sqlite3
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for,
    current_app, g)
from flask.cli import with_appcontext
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite.db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

@app.route("/")
@app.route("/get_items")
def get_items():
    items = mongo.db.items.find()
    return render_template("items.html", items=items)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)