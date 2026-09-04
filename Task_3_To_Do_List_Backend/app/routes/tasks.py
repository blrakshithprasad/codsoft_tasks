from datetime import date
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app import db
from app.models import Task
tasks_bp=Blueprint("tasks",__name__)
VALID_PRIORITY={"low","medium","high"}

def payload(d,existing=None):
    errors={}
    title=d.get("title",existing.title if existing else None)
    if not isinstance(title,str) or not title.strip():errors["title"]="Title is required."
    priority=d.get("priority",existing.priority if existing else "medium")
    if priority not in VALID_PRIORITY:errors["priority"]="priority must be low, medium or high."
    due=d.get("due_date",existing.due_date.isoformat() if existing and existing.due_date else None)
    parsed=None
    if due:
        try:parsed=date.fromisoformat(due)
        except ValueError:errors["due_date"]="Use YYYY-MM-DD."
    return errors,{"title":title.strip(),"description":d.get("description",existing.description if existing else ""), "completed":d.get("completed",existing.completed if existing else False),"priority":priority,"category":d.get("category",existing.category if existing else "general"),"due_date":parsed}

@tasks_bp.get("")
@jwt_required()
def list_tasks():
    uid=get_jwt_identity();q=Task.query.filter_by(user_id=uid)
    status=request.args.get("status")
    if status in {"completed","pending"}:q=q.filter_by(completed=status=="completed")
    search=request.args.get("q","").strip()
    if search:q=q.filter(Task.title.ilike(f"%{search}%")|Task.description.ilike(f"%{search}%"))
    category=request.args.get("category")
    if category:q=q.filter_by(category=category)
    page=max(request.args.get("page",1,type=int),1);per_page=min(max(request.args.get("per_page",10,type=int),1),100)
    p=q.order_by(Task.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    return jsonify({"data":[x.to_dict() for x in p.items],"pagination":{"page":p.page,"per_page":p.per_page,"pages":p.pages,"total":p.total}})

@tasks_bp.post("")
@jwt_required()
def create():
    d=request.get_json(silent=True) or {};e,data=payload(d)
    if e:return jsonify({"error":"Validation failed","details":e}),400
    t=Task(user_id=get_jwt_identity(),**data);db.session.add(t);db.session.commit();return jsonify(t.to_dict()),201

@tasks_bp.get("/<int:id>")
@jwt_required()
def get(id):
    t=Task.query.filter_by(id=id,user_id=get_jwt_identity()).first()
    return (jsonify(t.to_dict()),200) if t else (jsonify({"error":"Task not found"}),404)

@tasks_bp.put("/<int:id>")
@jwt_required()
def update(id):
    t=Task.query.filter_by(id=id,user_id=get_jwt_identity()).first()
    if not t:return jsonify({"error":"Task not found"}),404
    e,data=payload(request.get_json(silent=True) or {},t)
    if e:return jsonify({"error":"Validation failed","details":e}),400
    for k,v in data.items():setattr(t,k,v)
    db.session.commit();return jsonify(t.to_dict())

@tasks_bp.patch("/<int:id>/status")
@jwt_required()
def status(id):
    t=Task.query.filter_by(id=id,user_id=get_jwt_identity()).first()
    if not t:return jsonify({"error":"Task not found"}),404
    d=request.get_json(silent=True) or {}
    if not isinstance(d.get("completed"),bool):return jsonify({"error":"completed must be boolean"}),400
    t.completed=d["completed"];db.session.commit();return jsonify(t.to_dict())

@tasks_bp.delete("/<int:id>")
@jwt_required()
def delete(id):
    t=Task.query.filter_by(id=id,user_id=get_jwt_identity()).first()
    if not t:return jsonify({"error":"Task not found"}),404
    db.session.delete(t);db.session.commit();return jsonify({"message":"Task deleted"})
