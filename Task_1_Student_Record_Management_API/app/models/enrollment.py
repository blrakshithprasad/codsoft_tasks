from app import db
class Enrollment(db.Model):
    __tablename__="enrollments"
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)
    semester=db.Column(db.String(30),nullable=False)
    student=db.relationship("Student",back_populates="enrollments")
    course=db.relationship("Course",back_populates="enrollments")
    __table_args__=(db.UniqueConstraint("student_id","course_id","semester",name="uq_student_course_semester"),)
    def to_dict(self):
        return {"id":self.id,"student_id":self.student_id,"course_id":self.course_id,"semester":self.semester}
