from datetime import datetime
from models import db, User, Yacht, Booking
from app import app

# Ensure to run this script within the application context
with app.app_context():
    # Drop all existing data and create fresh tables
    db.drop_all()
    db.create_all()

    # Sample Users
    user1 = User(username='user1', email='user1@example.com', password='password1')
    user2 = User(username='user2', email='user2@example.com', password='password2')

    # # Sample Yachts
    # yacht1 = Yacht(name='Azam', description='Luxury yacht with modern amenities', capacity=1000, price=36428.24, image='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.luxuryachts.eu%2Fluxury-yachts%2Fluxury-yacht-of-the-week-the-super-yacht-azzam&psig=AOvVaw3QwMHzgYZOwMFJZ5t1Wfz9&ust=1720694666330000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCIiz8amlnIcDFQAAAAAdAAAAABAE')
    # yacht2 = Yacht(name='Eclipse', description='Spacious yacht with a swimming pool', capacity=2500, price=61069.75, image='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vesselfinder.com%2Fvessels%2Fdetails%2F1009613&psig=AOvVaw13310fON2QrOqC7JVcufpN&ust=1720695241580000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMj0pbynnIcDFQAAAAAdAAAAABAE')
    
    # Sample Bookings
    booking1 = Booking(yacht_id=1, start_date=datetime(2024, 8, 1), end_date=datetime(2024, 8, 7), status='confirmed')
    booking2 = Booking(yacht_id=2, start_date=datetime(2024, 9, 10), end_date=datetime(2024, 9, 15), status='pending')
    
    # Add the instances to the session and commit to the database
    db.session.add_all([user1, user2,  booking1, booking2])
    db.session.commit()
    
    print("Database populated with sample data.")
