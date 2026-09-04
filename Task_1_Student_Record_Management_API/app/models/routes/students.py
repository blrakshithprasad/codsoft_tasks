from flask import Blueprint,request,jsonify
from sqlalchemy import or_
from app import db
from app.models import Student
from app.utils.validation import validate_student

students_bp=Blueprint("students",__name__)

@students_bp.get("")
def list_students():
    q=request.args.get("q","").strip()
    department=request.args.get("department")
    sort=request.args.get("sort","id")
    order=request.args.get("order","asc")
    page=max(request.args.get("page",1,type=int),1); per_page=min(max(request.args.get("per_page",10,type=int),1),100)
    allowed={"id":Student.id,"name":Student.name,"email":Student.email,"age":Student.age,"department":Student.department}
    query=Student.query
    if q: query=query.filter(or_(Student.name.ilike(f"%{q}%"),Student.email.ilike(f"%{q}%")))
    if department: query=query.filter(Student.department.ilike(department))
    col=allowed.get(sort,Student.id); query=query.order_by(col.desc() if order=="desc" else col.asc())
    data=query.paginate(page=page,per_page=per_page,error_out=False)
    return jsonify({"data":[x.to_dict() for x in data.items],"pagination":{"page":data.page,"per_page":data.per_page,"pages":data.pages,"total":data.total}})

@students_bp.post("")
def create_student():
    data=request.get_json(silent=True) or {}; errors=validate_student(data)
    if errors:return jsonify({"error":"Validation failed","details":errors}),400
    if Student.query.filter_by(email=data["email"]).first(): return jsonify({"error":"Email already exists"}),409
    s=Student(name=data["name"].strip(),email=data["email"].lower(),age=data["age"],department=data["department"].strip())
    db.session.add(s); db.session.commit()
    return jsonify(s.to_dict()),201

@students_bp.get("/<int:id>")
def get_student(id):
    s=db.session.get(Student,id)
    return (jsonify(s.to_dict()),200) if s else (jsonify({"error":"Student not found"}),404)

@students_bp.put("/<int:id>")
def update_student(id):
    s=db.session.get(Student,id)
    if not s:return jsonify({"error":"Student not found"}),404
    data=request.get_json(silent=True) or {}; errors=validate_student(data)
    if errors:return jsonify({"error":"Validation failed","details":errors}),400
    if Student.query.filter(Student.email==data["email"].lower(),Student.id!=id).first():return jsonify({"error":"Email already exists"}),409
    s.name=data["name"].strip();s.email=data["email"].lower();s.age=data["age"];s.department=data["department"].strip()
    db.session.commit();return jsonify(s.to_dict())

@students_bp.delete("/<int:id>")
def delete_student(id):
    s=db.session.get(Student,id)
    if not s:return jsonify({"error":"Student not found"}),404
    db.session.delete(s);db.session.commit();return jsonify({"message":"Student deleted"})
