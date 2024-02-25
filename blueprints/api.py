from flask import jsonify, Blueprint, request
from models import User, db
from flask_jwt_extended import jwt_required, create_access_token


api = Blueprint('api_endpoint', __name__)

def error(msg):
    return jsonify(error={
        "message": f"{msg}"
    })


@api.route('/api/generate/')
def generate_token():
    token = request.args.get("token")
    if token == "secret":
        access_token = create_access_token(identity=token)
        return jsonify(access_token=access_token)
    else:
        return error("Invalid token")


@api.route('/api/user/<int:id>')
@jwt_required(locations=["headers"])
def user(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    
    if user:
        return jsonify(user={
            "name": user.name,
            "email": user.email
        })
    else:
        return error("Unable to find the user")