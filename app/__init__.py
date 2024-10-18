from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .selenium_controller import bp as selenium_bp


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(selenium_bp)

    return app

