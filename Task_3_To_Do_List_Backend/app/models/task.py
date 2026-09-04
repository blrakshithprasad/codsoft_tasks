from app import db
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,index=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text,default="")
    completed=db.Column(db.Boolean,default=False,nullable=False,index=True)
    due_date=db.Column(db.Date,nullable=True)
    priority=db.Column(db.String(20),default="medium",nullable=False)
    category=db.Column(db.String(80),default="general",nullable=False)
    user=db.relationship("User",back_populates="tasks")
    def to_dict(self):
        return {"id":self.id,"title":self.title,"description":self.description,"completed":self.completed,"due_date":self.due_date.isoformat() if self.due_date else None,"priority":self.priority,"category":self.category}
