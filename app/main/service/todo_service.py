import uuid
import datetime

from app.main import db
from app.main.model.todo import Todo
from app.main.service.auth_helper import Auth

def save_new_todo(data):
    user_details = Auth.login_info(request)

    new_user = Todo(
        public_id=str(uuid.uuid4()),
        email=data['text'],
        username=data['username'],
        password=data['password'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(new_user)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all_todos():
    return Todo.query.all()


def get_a_todo(public_id):
    return Todo.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
