from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models import User
auth_bp=Blueprint("auth",__name__)

@auth_bp.post("/register")
def register():
    d=request.get_json(silent=True) or {}
    if not d.get("username") or not d.get("password") or len(d["password"])<8:return jsonify({"error":"username and password (min 8 chars) are required"}),400
    if User.query.filter_by(username=d["username"]).first():return jsonify({"error":"Username already exists"}),409
    u=User(username=d["username"].strip());u.set_password(d["password"]);db.session.add(u);db.session.commit()
    return jsonify({"message":"Registered","access_token":create_access_token(identity=u.id)}),201

@auth_bp.post("/login")
def login():
    d=request.get_json(silent=True) or {};u=User.query.filter_by(username=d.get("username","")).first()
    if not u or not u.check_password(d.get("password","")):return jsonify({"error":"Invalid credentials"}),401
    return jsonify({"access_token":create_access_token(identity=u.id)})
