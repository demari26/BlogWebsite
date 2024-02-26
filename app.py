from flask import Flask, redirect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from flask_gravatar import Gravatar

from models import db, User
from config import Config

from blueprints import guest, user, api, ai

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    migrate = Migrate(app, db)
    ckeditor = CKEditor(app)
    bootstrap = Bootstrap5(app)
    jwt = JWTManager(app)
    gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)
   
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(guest.guest)
    app.register_blueprint(user.authenticated_user)
    app.register_blueprint(api.api)
    app.register_blueprint(ai.ai)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect('/login')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
