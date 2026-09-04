from app import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id":self.id,"name":self.name,"email":self.email,"age":self.age,"department":self.department}
