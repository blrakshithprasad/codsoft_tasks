from flask import Blueprint,request,jsonify
from app import db
from app.models import Course
from app.utils.validation import validate_course
courses_bp=Blueprint("courses",__name__)

@courses_bp.get("")
def list_courses():
    q=request.args.get("q",""); page=max(request.args.get("page",1,type=int),1); per_page=min(max(request.args.get("per_page",10,type=int),1),100)
    sort=request.args.get("sort","id"); order=request.args.get("order","asc")
    cols={"id":Course.id,"code":Course.code,"name":Course.name,"credits":Course.credits}
    query=Course.query
    if q: query=query.filter(Course.name.ilike(f"%{q}%")|Course.code.ilike(f"%{q}%"))
    col=cols.get(sort,Course.id);query=query.order_by(col.desc() if order=="desc" else col.asc())
    data=query.paginate(page=page,per_page=per_page,error_out=False)
    return jsonify({"data":[x.to_dict() for x in data.items],"pagination":{"page":data.page,"per_page":data.per_page,"pages":data.pages,"total":data.total}})

@courses_bp.post("")
def create_course():
    data=request.get_json(silent=True) or {};errors=validate_course(data)
    if errors:return jsonify({"error":"Validation failed","details":errors}),400
    if Course.query.filter_by(code=data["code"].upper()).first():return jsonify({"error":"Course code exists"}),409
    c=Course(code=data["code"].upper(),name=data["name"].strip(),credits=data["credits"]);db.session.add(c);db.session.commit()
    return jsonify(c.to_dict()),201

@courses_bp.get("/<int:id>")
def get_course(id):
    c=db.session.get(Course,id);return (jsonify(c.to_dict()),200) if c else (jsonify({"error":"Course not found"}),404)

@courses_bp.put("/<int:id>")
def update_course(id):
    c=db.session.get(Course,id)
    if not c:return jsonify({"error":"Course not found"}),404
    data=request.get_json(silent=True) or {};errors=validate_course(data)
    if errors:return jsonify({"error":"Validation failed","details":errors}),400
    if Course.query.filter(Course.code==data["code"].upper(),Course.id!=id).first():return jsonify({"error":"Course code exists"}),409
    c.code=data["code"].upper();c.name=data["name"].strip();c.credits=data["credits"];db.session.commit();return jsonify(c.to_dict())

@courses_bp.delete("/<int:id>")
def delete_course(id):
    c=db.session.get(Course,id)
    if not c:return jsonify({"error":"Course not found"}),404
    db.session.delete(c);db.session.commit();return jsonify({"message":"Course deleted"})
