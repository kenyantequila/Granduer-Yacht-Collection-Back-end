# Yacht Blueprint
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import db,  Yacht,Booking
from flask_cors import CORS


from flask_cors import CORS
yachts_bp = Blueprint('yachts', __name__, url_prefix='/yachts')
api_yachts = Api(yachts_bp)
yacht_parser = reqparse.RequestParser()
yacht_parser.add_argument('name', type=str, required=True, help='Name is required')
yacht_parser.add_argument('description', type=str, required=True, help='Description is required')
yacht_parser.add_argument('capacity', type=int, required=True, help='Capacity is required')
yacht_parser.add_argument('price', type=float, required=True, help='Price is required')
yacht_parser.add_argument('image', type=str, required=True, help='Image URL is required')
CORS(yachts_bp)

class YachtResource(Resource):
    def get(self, id):
        yacht = Yacht.query.get_or_404(id)
        return {
            'id': yacht.id,
            'name': yacht.name,
            'description': yacht.description,
            'capacity': yacht.capacity,
            'price': yacht.price,
            'image': yacht.image
        }

    def put(self, id):
        data = yacht_parser.parse_args()
        yacht = Yacht.query.get_or_404(id)
        yacht.name = data['name']
        yacht.description = data['description']
        yacht.capacity = data['capacity']
        yacht.price = data['price']
        yacht.image = data['image']
        db.session.commit()
        return {
            'id': yacht.id,
            'name': yacht.name,
            'description': yacht.description,
            'capacity': yacht.capacity,
            'price': yacht.price,
            'image': yacht.image
        }

    def delete(self, id):
        try:
            yacht = Yacht.query.get_or_404(id)
            db.session.delete(yacht)
            db.session.commit()
            return {'message': 'Yacht deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to delete yacht', 'error': str(e)}, 500

api_yachts.add_resource(YachtResource, '/<int:id>')

class YachtList(Resource):
    def get(self):
        yachts = Yacht.query.all()
        return [{'id': yacht.id, 'name': yacht.name, 'description': yacht.description, 'capacity': yacht.capacity, 'price': yacht.price, 'image': yacht.image} for yacht in yachts]
    
    def post(self):
        data = yacht_parser.parse_args()
        new_yacht = Yacht(name=data['name'], description=data['description'], capacity=data['capacity'], price=data['price'], image=data['image'])
        db.session.add(new_yacht)
        db.session.commit()
        return {'message': 'Yacht successfully created'}

api_yachts.add_resource(YachtList, '/yachtlist')


class yachtbookingResource(Resource):
    def get(self, yacht_id):
        bookings = Booking.query.filter_by(yacht_id=yacht_id).all()
        return [{'id': booking.id, 'user_id': booking.user_id,'start_date': booking.start_date, 'end_date': booking.end_date,'status': booking.status} for booking in bookings]


api_yachts.add_resource(yachtbookingResource,'/bookings')