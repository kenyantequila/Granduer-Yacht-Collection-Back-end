from app import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yacht_id = db.Column(db.Integer, db.ForeignKey('yacht.id'), nullable=False)
    yacht = db.relationship('Yacht', backref=db.backref('bookings', lazy=True))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')

    def __repr__(self):
        return f"Booking('{self.yacht.name}', {self.start_date}, {self.end_date}, '{self.status}')"