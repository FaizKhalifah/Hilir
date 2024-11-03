from app.utils.db import db
from app.models.base import BaseModel
from datetime import date

class Child(BaseModel):
    __tablename__ = "children"

    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=False)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
