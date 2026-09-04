from flask import Blueprint,request,jsonify
from sqlalchemy import or_
from app import db
from app.models import Contact
from app.utils.validation import validate
contacts_bp=Blueprint("contacts",__name__)

def paginate(query):
    page=max(request.args.get("page",1,type=int),1); per_page=min(max(request.args.get("per_page",10,type=int),1),100)
    sort=request.args.get("sort","name");order=request.args.get("order","asc")
    cols={"id":Contact.id,"name":Contact.name,"email":Contact.email,"company":Contact.company}
    col=cols.get(sort,Contact.name)
    query=query.order_by(col.desc() if order=="desc" else col.asc())
    p=query.paginate(page=page,per_page=per_page,error_out=False)
    return {"data":[x.to_dict() for x in p.items],"pagination":{"page":p.page,"per_page":p.per_page,"pages":p.pages,"total":p.total}}

@contacts_bp.get("")
def list_contacts():
    q=request.args.get("q","").strip()
    query=Contact.query
    if q:
        like=f"%{q}%";query=query.filter(or_(Contact.name.ilike(like),Contact.email.ilike(like),Contact.phone.ilike(like)))
    return jsonify(paginate(query))

@contacts_bp.post("")
def create():
    data=request.get_json(silent=True) or {};e=validate(data)
    if e:return jsonify({"error":"Validation failed","details":e}),400
    email=data["email"].lower().strip();phone=data["phone"].strip()
    if Contact.query.filter_by(email=email).first() or Contact.query.filter_by(phone=phone).first():return jsonify({"error":"Duplicate contact"}),409
    c=Contact(name=data["name"].strip(),email=email,phone=phone,address=data.get("address","").strip(),company=data.get("company","").strip())
    db.session.add(c);db.session.commit();return jsonify(c.to_dict()),201

@contacts_bp.get("/<int:id>")
def get(id):
    c=db.session.get(Contact,id);return (jsonify(c.to_dict()),200) if c else (jsonify({"error":"Contact not found"}),404)

@contacts_bp.put("/<int:id>")
def update(id):
    c=db.session.get(Contact,id)
    if not c:return jsonify({"error":"Contact not found"}),404
    data=request.get_json(silent=True) or {};e=validate(data)
    if e:return jsonify({"error":"Validation failed","details":e}),400
    email=data["email"].lower().strip();phone=data["phone"].strip()
    if Contact.query.filter(Contact.id!=id,or_(Contact.email==email,Contact.phone==phone)).first():return jsonify({"error":"Duplicate contact"}),409
    c.name=data["name"].strip();c.email=email;c.phone=phone;c.address=data.get("address","").strip();c.company=data.get("company","").strip()
    db.session.commit();return jsonify(c.to_dict())

@contacts_bp.delete("/<int:id>")
def delete(id):
    c=db.session.get(Contact,id)
    if not c:return jsonify({"error":"Contact not found"}),404
    db.session.delete(c);db.session.commit();return jsonify({"message":"Contact deleted"})
