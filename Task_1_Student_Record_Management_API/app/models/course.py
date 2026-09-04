from app import db
class Course(db.Model):
    __tablename__="courses"
    id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(30),unique=True,nullable=False,index=True)
    name=db.Column(db.String(150),nullable=False)
    credits=db.Column(db.Integer,nullable=False)
    enrollments=db.relationship("Enrollment",back_populates="course",cascade="all, delete-orphan")
    def to_dict(self):
        return {"id":self.id,"code":self.code,"name":self.name,"credits":self.credits}
