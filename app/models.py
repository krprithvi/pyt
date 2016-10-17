from app import db
from hashlib import md5
# Store tutorials in the database
class Tut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(65000), nullable=False)
    question = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Tutorial %r>" % self.name
# Store quizzes in the database
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Quiz %r>" % self.name
