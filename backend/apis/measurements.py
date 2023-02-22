from flask import request
from flask_restx import Namespace, Resource, fields
from flask_restx.reqparse import RequestParser
from bson.objectid import ObjectId

from core import db_client
from core.utils import decode_auth_token

import jwt

api = Namespace('measurements', description='Measurement related operations')

token_request = RequestParser()
token_request.add_argument('Authorization', required=True,
                           location='headers', help='your authorization token')

chest_payload = api.model('Chest info', {
    'bust': fields.Float(required=True, description='bust size'),
    'waist': fields.Float(required=True, description='waist size'),
    'hips': fields.Float(required=True, description='hip size'),
})


@api.route('/chest')
class Chest(Resource):

    @api.expect(token_request)
    def get(self):
        print(f'using token {request.headers["Authorization"]}')
        try:
            sub = decode_auth_token(request.headers['Authorization'])
        except jwt.ExpiredSignatureError:
            return {'success': False, 'reason': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'success': False, 'reason': 'Invalid token. Please log in again.'}

        chest = db_client.get_database('measurements').get_collection('chest')
        search = chest.find({'uid': sub}, {'_id': False})

        return list(search)

    @api.expect(token_request, chest_payload)
    def post(self):
        payload = request.get_json()

        try:
            sub = decode_auth_token(request.headers['Authorization'])
        except jwt.ExpiredSignatureError:
            return {'success': False, 'reason': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'success': False, 'reason': 'Invalid token. Please log in again.'}

        payload['uid'] = sub
        chest = db_client.get_database('measurements').get_collection('chest')
        chest.insert_one(payload)

        return {'success': True, 'reason': 'data logged'}
