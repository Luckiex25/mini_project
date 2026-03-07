from flask import Flask
from .extensions import db, login_manager
from .models import User, Bag

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'bagstore-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from .core.routes import core_bp
    from .users.routes import users_bp
    from .bags.routes import bags_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(bags_bp)

    with app.app_context():
        db.create_all()
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))