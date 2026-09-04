import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
def create_app(test_config=None):
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL","sqlite:///contacts.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    if test_config: app.config.update(test_config)
    db.init_app(app)
    from app.routes.contacts import contacts_bp
    app.register_blueprint(contacts_bp,url_prefix="/api/contacts")
    with app.app_context(): db.create_all()
    return app
