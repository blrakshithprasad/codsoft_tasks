from app import db
class Contact(db.Model):
    __tablename__="contacts"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(255),nullable=False,index=True)
    phone=db.Column(db.String(30),nullable=False,index=True)
    address=db.Column(db.String(255),default="")
    company=db.Column(db.String(150),default="")
    __table_args__=(db.UniqueConstraint("email","phone",name="uq_contact_identity"),)
    def to_dict(self):
        return {c:getattr(self,c) for c in ["id","name","email","phone","address","company"]}
