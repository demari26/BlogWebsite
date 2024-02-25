from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from models import db, User
from config import Config

from blueprints import guest, user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    migrate = Migrate(app, db)
    ckeditor = CKEditor(app)
    bootstrap = Bootstrap5(app)
   
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(guest.guest)
    app.register_blueprint(user.authenticated_user)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)