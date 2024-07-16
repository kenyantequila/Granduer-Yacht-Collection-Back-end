# Booking Blueprint
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import db,  Booking

from flask_cors import CORS
bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')
api_bookings = Api(bookings_bp)
booking_parser = reqparse.RequestParser()
booking_parser.add_argument('yacht_id', type=int, required=True, help='Yacht ID is required')
booking_parser.add_argument('start_date', type=str, required=True, help='Start date is required')
booking_parser.add_argument('end_date', type=str, required=True, help='End date is required')
booking_parser.add_argument('status', type=str, required=False, default='pending')
CORS(bookings_bp)

class BookingResource(Resource):
    def get(self, id):
        booking = Booking.query.get_or_404(id)
        return {'id': booking.id, 'yacht_id': booking.yacht_id, 'start_date': booking.start_date, 'end_date': booking.end_date, 'status': booking.status}
    
    def put(self, id):
        data = booking_parser.parse_args()
        booking = Booking.query.get_or_404(id)
        booking.yacht_id = data['yacht_id']
        booking.start_date = data['start_date']
        booking.end_date = data['end_date']
        booking.status = data['status']
        db.session.commit()
        return {'id': booking.id, 'yacht_id': booking.yacht_id, 'start_date': booking.start_date, 'end_date': booking.end_date, 'status': booking.status}
    
    def delete(self, id):
        booking = Booking.query.get_or_404(id)
        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking deleted successfully'}

api_bookings.add_resource(BookingResource, '/<int:id>')

class BookingList(Resource):
    def get(self):
        bookings = Booking.query.all()
        return [{'id': booking.id, 'yacht_id': booking.yacht_id, 'start_date': booking.start_date, 'end_date': booking.end_date, 'status': booking.status} for booking in bookings]
    
    def post(self):
        data = booking_parser.parse_args()
        new_booking = Booking(yacht_id=data['yacht_id'], start_date=data['start_date'], end_date=data['end_date'], status=data['status'])
        db.session.add(new_booking)
        db.session.commit()
        return {'message': 'Booking successfully created'}

api_bookings.add_resource(BookingList, '/bookinglist')