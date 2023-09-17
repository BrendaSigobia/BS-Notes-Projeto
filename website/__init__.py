from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
NOME_BD = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b1006033gs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOME_BD}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuario

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    return app


def criar_db(app):
    if not path.exists('website/' + NOME_BD):
        db.create_all(app=app)
        print('Banco de dados criado!')
    if not os.path.exists('website/' + NOME_BD):
        with app.app_context():
            db.create_all()
            print('Banco de dados criado!')
