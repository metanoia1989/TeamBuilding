#!/usr/bin/env python3
# -*- conding:utf8 -*-


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)

api = Api(app)

# 要操作的资源类型
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

# 解析请求参数
parser = reqparse.RequestParser()
parser.add_argument('task') 

# 操作(put / get / delete)单一资源
class Todo(Resource):
    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id], 200
    
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

# 操作(post/get)资源列表
class TodoList(Resource):
    def get(self):
        return TODOS, 200
    
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    
# 路由
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)