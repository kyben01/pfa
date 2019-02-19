from flask import request
from flask_restplus import Resource, Namespace

from app.main import db
from app.main.model.todo import Todo
from app.main.util.decorator import admin_token_required
from app.main.service.auth_helper import Auth

import datetime

api = Namespace('todo', description='authentication related operations')

@api.route('/v1')
class TodoList(Resource):
    """
        Todo Resource
    """
    @api.doc('Get All Todo\'s')
    @admin_token_required
    def get(self):
        """List all Todo's"""
        user_details = Auth.login_info(request)
        todos = Todo.query.filter_by(author = user_details["user_id"]).all()
        output = []
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['text'] = todo.text
            todo_data['complete'] = todo.complete
            output.append(todo_data)
        return {"todos":output}, 201
    @api.doc("Create New Todo")

    @admin_token_required
    def post(self):
        """Create new Todo's"""
        user_details = Auth.login_info(request)
        data = request.get_json()

        new_todo = Todo(
            text = data["text"],
            complete = False,
            author = user_details["user_id"],
            datecreated = datetime.datetime.utcnow()
        )

        db.session.add(new_todo)
        db.session.commit()

        response_object = {
        'status': 'success',
        'message': "Todo created!"
        }
        return response_object, 201

@api.route('/v1/<todo_id>')
class TodoList(Resource):

    @api.doc('Get Single Todo\'s')
    @admin_token_required
    def get(self, todo_id):
        user_details = Auth.login_info(request)
        todo = Todo.query.filter_by(id=todo_id, author=user_details["user_id"]).first()
        if not todo:
            return {"error":"Todo's not found!"}, 404
        todo_data = {}
        # todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        return todo_data


    @api.doc('Update Todo\'s')
    @admin_token_required
    def put(self, todo_id):
        data = request.get_json()
        user_details = Auth.login_info(request)
        todo = Todo.query.filter_by(id=todo_id, author=user_details["user_id"]).first()
        if not todo:
            return {"error":"Todo's not found!"}, 404
        todo.complete = True
        todo.text = data["text"]
        db.session.commit()
        return {'message' : 'Todo item has been completed!'}, 201


    @api.doc('Delete Todo\'s')
    @admin_token_required
    def delete(self, todo_id):
        data = request.get_json()
        user_details = Auth.login_info(request)
        todo = Todo.query.filter_by(id=todo_id, author=user_details["user_id"]).first()
        if not todo:
            return {"error":"Todo's not found!"}, 404

        db.session.delete(todo)
        db.session.commit()
        return {'message' : 'Todo item deleted!'}, 201
