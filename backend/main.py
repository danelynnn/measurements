from flask import Flask, request
from flask_restx import Resource, Api, fields
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
db_client = MongoClient('mongodb+srv://danelynnn:s99UMbDSv5zZRzSV@cluster0.qucl8rc.mongodb.net/retryWrites=true&w=majority')
SALT = bytes('salty', 'utf-8')
scrypt = Scrypt(SALT, 32, 2**14, 8, 1)


register = api.model('Register', {
    'username': fields.String(required=True, description='username to register'),
    'email': fields.String(required=True, description='email of user'),
    'password': fields.String(required=True, description='password of which to register'),
})
@api.route('/register')
class Register(Resource):

    @api.expect(register)
    def post(self):
        username, email, password = list(request.get_json().values())
        users = db_client.get_database('measurements').get_collection('users')

        if not list(users.find({'$or': [{'username': username}, {'email': email}]})):
            pw_hash = scrypt.derive(bytes(password, 'utf-8'))
            users.insert_one({'username': username, 'password': pw_hash, 'email': email})
            return {'success': True, 'reason': f'user created with username {username}'}
        else:
            return {'success': False, 'reason': 'user already exists!'}

login = api.model('Login', {
    'username': fields.String(required=True, description='username to login'),
    'password': fields.String(required=True, description='password of which to login'),
})
@api.route('/login')
class Login(Resource):
    @api.expect(login)
    def post(self):
        username, password = list(request.get_json().values())
        
        users = db_client.get_database('measurements').get_collection('users')
        search = users.find({'$or': [{'username': username}, {'email': username}]})

        result = next(search, None)
        if result:
            try:
                scrypt.verify(bytes(password, 'utf-8'), result['password'])
            except:
                return {'success': False, 'reason': 'password incorrect'}

            return {'success': True, 'reason': 'user logged in!'}
        else:
            return {'success': False, 'reason': 'user not found'}

@api.route('/measurements')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
