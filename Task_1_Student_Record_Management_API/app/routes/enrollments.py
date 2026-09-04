from flask import Blueprint,request,jsonify
from app import db
from app.models import Enrollment,Student,Course
from app.utils.validation import validate_enrollment
enrollments_bp=Blueprint("enrollments",__name__)

@enrollments_bp.get("")
def list_enrollments():
    page=max(request.args.get("page",1,type=int),1);per_page=min(max(request.args.get("per_page",10,type=int),1),100)
    student_id=request.args.get("student_id",type=int);course_id=request.args.get("course_id",type=int)
    q=Enrollment.query
    if student_id:q=q.filter_by(student_id=student_id)
    if course_id:q=q.filter_by(course_id=course_id)
    data=q.order_by(Enrollment.id.asc()).paginate(page=page,per_page=per_page,error_out=False)
    return jsonify({"data":[x.to_dict() for x in data.items],"pagination":{"page":data.page,"per_page":data.per_page,"pages":data.pages,"total":data.total}})

@enrollments_bp.post("")
def create_enrollment():
    data=request.get_json(silent=True) or {};errors=validate_enrollment(data)
    if errors:return jsonify({"error":"Validation failed","details":errors}),400
    if not db.session.get(Student,data["student_id"]) or not db.session.get(Course,data["course_id"]):return jsonify({"error":"Student or course not found"}),404
    if Enrollment.query.filter_by(student_id=data["student_id"],course_id=data["course_id"],semester=data["semester"]).first():return jsonify({"error":"Duplicate enrollment"}),409
    e=Enrollment(**data);db.session.add(e);db.session.commit();return jsonify(e.to_dict()),201

@enrollments_bp.get("/<int:id>")
def get_enrollment(id):
    e=db.session.get(Enrollment,id);return (jsonify(e.to_dict()),200) if e else (jsonify({"error":"Enrollment not found"}),404)

@enrollments_bp.delete("/<int:id>")
def delete_enrollment(id):
    e=db.session.get(Enrollment,id)
    if not e:return jsonify({"error":"Enrollment not found"}),404
    db.session.delete(e);db.session.commit();return jsonify({"message":"Enrollment deleted"})
