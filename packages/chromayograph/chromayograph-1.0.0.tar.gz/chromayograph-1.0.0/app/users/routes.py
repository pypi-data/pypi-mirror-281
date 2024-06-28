from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/users')

