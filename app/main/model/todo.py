from .. import db
import datetime


class Todo(db.Model):
    """
        Todo Model
    """
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(500), nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    author = db.Column(db.String(100), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False)
