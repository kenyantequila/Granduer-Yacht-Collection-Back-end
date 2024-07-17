from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy( metadata=metadata)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

class Yacht(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)  # New column for image URL

    
    def __repr__(self):
        return f"Yacht('{self.name}', '{self.description}', {self.capacity}, {self.price})"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yacht_id = db.Column(db.Integer, db.ForeignKey('yacht.id'), nullable=False)
    yacht = db.relationship('Yacht', backref=db.backref('bookings', lazy=True))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')

    def __repr__(self):
        return f"Booking('{self.yacht.first_name}', {self.start_date.strftime('%Y-%m-%d')}, {self.end_date.strftime('%Y-%m-%d')}, '{self.status}')"