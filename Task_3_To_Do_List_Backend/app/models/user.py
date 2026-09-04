from werkzeug.security import generate_password_hash,check_password_hash
from app import db
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)
    tasks=db.relationship("Task",back_populates="user",cascade="all,delete-orphan")
    def set_password(self,p):self.password_hash=generate_password_hash(p)
    def check_password(self,p):return check_password_hash(self.password_hash,p)
