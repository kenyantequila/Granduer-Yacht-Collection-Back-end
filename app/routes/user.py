from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import db,  User
from flask_cors import CORS


from flask_cors import CORS
users_bp = Blueprint('users', __name__, url_prefix='/users')
api_users = Api(users_bp)
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')
CORS(users_bp)

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return {'id': user.id, 'username': user.username, 'email': user.email}
    
    def put(self, id):
        data = user_parser.parse_args()
        user = User.query.get_or_404(id)
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']
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

CORS(users_bp)