from flask import Flask, abort, render_template, redirect, url_for, flash
import os
from model import db
from flask_migrate import Migrate

def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
    db.init_app(app)
   
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

app_instance = app()

if __name__ == "__main__":
    app_instance.run(debug=False)
