from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)
CORS(app)
bcrypt = Bcrypt(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Yacht(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    bookings = db.relationship('Booking', backref='yacht', cascade='all, delete-orphan')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yacht_id = db.Column(db.Integer, db.ForeignKey('yacht.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    num_days = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def register_admin(username, password):
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()

users_bp = Blueprint('users', __name__, url_prefix='/users')
api_users = Api(users_bp)
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')
CORS(users_bp)

class AdminRegister(Resource):
    def post(self):
        data = request.get_json()
        new_admin = Admin(username=data['username'], password=data['password'])
        db.session.add(new_admin)
        db.session.commit()
        return {"message": "Admin registered successfully!"}, 201

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        admin = Admin.query.filter_by(username=data['username']).first()
        if admin and bcrypt.check_password_hash(admin.password, data['password']):
            return {"message": "Admin logged in successfully!"}, 200
        else:
            return {"message": "Invalid username or password"}, 401

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return {'id': user.id, 'username': user.username, 'email': user.email}

    def put(self, id):
        data = user_parser.parse_args()
        user = User.query.get_or_404(id)
        user.username = data['username']
        user.email = data['email']
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email}

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

api_users.add_resource(UserResource, '/<int:id>')

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    def post(self):
        data = user_parser.parse_args()
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User successfully created'}

api_users.add_resource(UserList, '/userlist')

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            return {'message': 'Login successful', 'user': {'id': user.id, 'username': user.username, 'email': user.email}}
        else:
            return {'message': 'Invalid username or password'}, 401

api_users.add_resource(UserLogin, '/login')

class AddYacht(Resource):
    def post(self):
        data = request.get_json()
        new_yacht = Yacht(
            name=data['name'],
            description=data['description'],
            capacity=data['capacity'],
            price=data['price'],
            image=data['image']
        )
        db.session.add(new_yacht)
        db.session.commit()
        return {"message": "Yacht added successfully!"}, 201

class YachtResource(Resource):
    def get(self):
        yachts = Yacht.query.all()
        return [{'id': yacht.id, 'name': yacht.name, 'description': yacht.description, 'capacity': yacht.capacity, 'price': yacht.price, 'image': yacht.image} for yacht in yachts]

    def post(self):
        data = request.get_json()
        new_yacht = Yacht(
            name=data['name'],
            description=data['description'],
            capacity=data['capacity'],
            price=data['price'],
            image=data['image']
        )
        db.session.add(new_yacht)
        db.session.commit()
        return {'message': 'Yacht added successfully'}, 201

    def put(self, yacht_id):
        data = request.get_json()
        yacht = Yacht.query.get_or_404(yacht_id)
        yacht.name = data['name']
        yacht.description = data['description']
        yacht.capacity = data['capacity']
        yacht.price = data['price']
        yacht.image = data['image']
        db.session.commit()
        return {'message': 'Yacht updated successfully'}

    def delete(self, yacht_id):
        try:
            print(f"Attempting to delete yacht with ID: {yacht_id}")  # Debug print
            yacht = Yacht.query.get_or_404(yacht_id)
            
            # Delete associated bookings
            Booking.query.filter_by(yacht_id=yacht_id).delete()
            
            db.session.delete(yacht)
            db.session.commit()
            return {'message': 'Yacht deleted successfully'}
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")  # Debug print
            return {'message': str(e)}, 500

api.add_resource(YachtResource, '/yachts', '/yachts/<int:yacht_id>')



class YachtBookingsResource(Resource):
    def get(self, yacht_id):
        bookings = Booking.query.filter_by(yacht_id=yacht_id).all()
        return [{'id': booking.id, 'num_tickets': booking.num_tickets, 'num_days': booking.num_days, 'total_price': booking.total_price, 'booking_date': booking.booking_date} for booking in bookings]

api.add_resource(YachtBookingsResource, '/yachts/<int:yacht_id>/bookings')

class BookingResource(Resource):
    def post(self):
        data = request.get_json()
        yacht_id = data['yacht_id']
        num_tickets = data['num_tickets']
        num_days = data['num_days']
        total_price = data['total_price']
        
        new_booking = Booking(yacht_id=yacht_id, num_tickets=num_tickets, num_days=num_days, total_price=total_price)
        db.session.add(new_booking)
        db.session.commit()
        return {'message': 'Booking created successfully'}, 201

api.add_resource(BookingResource, '/bookings')
api.add_resource(AdminRegister, '/admins/register')
api.add_resource(AdminLogin, '/admins/login')
api.add_resource(AddYacht, '/admin/add-yacht')
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True)
