"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


api = Blueprint('api', __name__)
CORS(api) # Allow CORS requests to this API

@api.route("/login", methods=["POST"])
def login():
    response_body = {}
    data = request.json
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
    #  TODO: realizar la logica para verificar en nuestra db
        response_body['message'] = 'Bad username or password'
        return response_body, 401
    access_token = create_access_token(identity={'username':username, 'user_id': 30})
    response_body['message'] = 'user logged'
    response_body['access_token'] = access_token
    # return jsonify(access_token=access_token)
    return response_body, 200

@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    response_body = {} # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    if current_user['user_id'] == 30:
        response_body['message'] = f'Acceso concedido a {current_user}'
        response_body['user_data']= current_user
        return response_body, 200
    response_body['message'] = f'acceso denegado porque no eres usuario 30'
    response_body['user_data'] = {}
    # return jsonify(logged_in_as=current_user), 200 
    return response_body, 200


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body["message"] =  "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return jsonify(response_body), 200
