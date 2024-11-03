from app.models.base import BaseModel
from app.utils.db import db

class Report(BaseModel):
    __tablename__ = "reports"

    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    report_data = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    child = db.relationship("Child", backref="reports", lazy=True)
