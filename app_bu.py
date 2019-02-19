#!flask/bin/python
# (TUTORIAL FROM:) https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime

from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootroot123@localhost/dbtodo'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
# AUTHINTICATION =================================================================================================================
#=================================================================================================================================
auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

# ADD URL TO THE GET RETURNED DATA  ==============================================================================================
#=================================================================================================================================
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# SAMPLE DATA OBJECT =============================================================================================================
#=================================================================================================================================
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# CUSTOM ERROR HUNDLER RETRUNED OBJECT ===========================================================================================
#=================================================================================================================================
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# GET METHOD =====================================================================================================================
#=================================================================================================================================
# (RETURN ALL) curl -i http://localhost:5000/todo/api/v1.0/tasks
# (AUTHINTICATION)  curl -i http://localhost:5000/todo/api/v1.0/tasks
# (AUTHINTICATION)  curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required #(AUTHINTICATION)
def get_tasks():
    # return jsonify({'tasks': tasks})
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

# (TEST = 200) curl -i http://localhost:5000/todo/api/v1.0/tasks/2
# (TEST = 404) curl -i http://localhost:5000/todo/api/v1.0/tasks/3
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# GET METHODD CONTROLLER
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})



# POST METHOD ====================================================================================================================
#=================================================================================================================================
# (TESY) curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
# POST METHOD CONTROLLER
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
# PUT METHOD =====================================================================================================================
#=================================================================================================================================
# (TEST) curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# DELETE METHOD ==================================================================================================================
#=================================================================================================================================
# (TEST) curl -i -X DELETE  http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


# USER GOES HERE

#######
## ADD NEW USER
#######
@app.route('/todo/api/v1.0/user', methods=['POST'])
@token_required
def add_user(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'task': 'New user created!'}), 201

#######
## GET ALL USER
#######
@app.route('/todo/api/v1.0/user', methods=['GET'])
@token_required
def get_all_user(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['user'] = current_user.admin
        output.append(user_data)
    return jsonify({'users' : output}) , 201


#######
## GET ONE USER
#######
@app.route('/todo/api/v1.0/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        # return jsonify({'message' : 'No user found!'})
        abort(404)

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

#######
## GET ONE USER
#######
@app.route('/todo/api/v1.0/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

#######
## DELETE USER
#######
@app.route('/todo/api/v1.0/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    db.session.delete(user)
    db.session.commit()

#######
## LOGIN
#######
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    return jsonify({'message' : 'The user has been deleted!'})

#######
## TODO-GET ALL
#######

@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'todos' : output})

######
## TODO-GET SINGLE
#######
@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify(todo_data)
######
## TODO-ADD RECORD
#######
@app.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message' : "Todo created!"})

######
## TODO-ADD RECORD
#######
@app.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})
    todo.complete = True
    db.session.commit()

    return jsonify({'message' : 'Todo item has been completed!'})

######
## TODO-ADD RECORD
#######
@app.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message' : 'Todo item deleted!'})


if __name__ == '__main__':
    app.run(debug=True)
