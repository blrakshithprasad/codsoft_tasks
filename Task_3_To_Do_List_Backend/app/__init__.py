import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
db=SQLAlchemy();jwt=JWTManager()
def create_app(test_config=None):
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL","sqlite:///todo.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY","dev-only-change-me")
    if test_config:app.config.update(test_config)
    db.init_app(app);jwt.init_app(app)
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp,url_prefix="/api/auth")
    app.register_blueprint(tasks_bp,url_prefix="/api/tasks")
    with app.app_context():db.create_all()
    return app
