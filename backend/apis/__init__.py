from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_restx.reqparse import RequestParser
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

api = Api(title='My Title',
          version='1.0',
          description='A description',)

from core import db_client, SALT
from core.utils import encode_auth_token

from apis.measurements import api as ns_measurements

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
            scrypt = Scrypt(SALT, 32, 2**14, 8, 1)
            pw_hash = scrypt.derive(bytes(password, 'utf-8'))
            users.insert_one(
                {'username': username, 'password': pw_hash, 'email': email})
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
        search = users.find(
            {'$or': [{'username': username}, {'email': username}]})

        result = next(search, None)
        if result:
            print(f'found user {result}')
            try:
                scrypt = Scrypt(SALT, 32, 2**14, 8, 1)
                scrypt.verify(bytes(password, 'utf-8'), result['password'])
            except:
                return {'success': False, 'reason': 'password incorrect'}

            auth_token = encode_auth_token(result)
            return {'success': True, 'reason': 'user logged in!', 'auth_token': auth_token}
        else:
            return {'success': False, 'reason': 'user not found'}


api.add_namespace(ns_measurements, path='/measurements')
