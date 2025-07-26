#Import Libraries
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

db = SQLAlchemy()

#Create Models(Tables)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)
    password = db.Column(db.String(30))
    expenses = db.relationship('Expense',backref='user',lazy=True)
    
class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))
    note = db.Column(db.String(500))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))