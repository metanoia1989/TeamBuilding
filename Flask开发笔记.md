# flask 开发资料
- [利用Python和Flask快速开发RESTful API](https://zhuanlan.zhihu.com/p/24629177) 
- [Python的Flask框架开发RESTful API](https://www.jianshu.com/p/ed1f819a7b58) 
- [Flask 开发 RESTful 接口](https://mindjet.github.io/coding/python/flask/python-flask-restful) 
- [Python从入门到秃顶 - 5](https://mindjet.github.io/coding/python/way2bald/python-way-to-bald-5) 
- [Flask 多模块开发](https://mindjet.github.io/coding/python/flask/flask-modular-application) 
- [Python进阶-IO](https://mindjet.github.io/coding/python/advanced/python-advanced-io) 
- [使用 Python 和 Flask 设计 RESTful API](http://www.pythondoc.com/flask-restful/first.html) 
- [The Flask Mega-Tutorial](http://www.pythondoc.com/flask-mega-tutorial/index.html) 
- [flask-restful api 文档](https://flask-restful.readthedocs.io/en/latest/api.html)
- [flask-restful english document](https://flask-restful.readthedocs.io/en/latest/quickstart.html) 
- [flask-restful 中文文档](http://www.pythondoc.com/Flask-RESTful/quickstart.html)
- [Flask RESTful API 开发----基础篇 (2)](https://blog.igevin.info/posts/flask-rest-basic-2/)
- [Flask 入门指南 - flask 开发用到的包和资料](https://blog.igevin.info/posts/flask-startup-guideline/)
- [RESTful API 编写指南 - 讲解了很多关于api开发的要点](https://blog.igevin.info/posts/restful-api-get-started-to-write/)

# 书籍资源
- [Flask Web开发实战 配套资源](http://helloflask.com/book/)

# 代码资源
- [flask 相关的代码片段](http://flask.pocoo.org/snippets/)

# 完善 api 需要完成的地方
简单的api只需要增删改查即可，但是一个完善的api有许多工作要完善
如何返回指定个数的资源，即limit操作。
如何指定资源返回时跳过的资源个数，即offset操作。
结合上边两条，如何实现分页，以及限定每页中资源的个数？
如何对返回的资源进行排序？
如何指定过滤条件？
如何实现批量操作？比如批量更新、批量删除等。
如何实现“请求验证”，即输入特定的用户名密码才会返回数据，否则认为非法请求。
如何处理各种异常？

# 感受
写 api 比 写整个web应用少了很多处理，后端不用再做那么事情，专心返回数据就好，界面数据交互、显示异常，都有js负责就好，而js本身就是非常好的。   
flask 的框架验证什么我没什么兴趣，了解就可以，不学也没关系，开发好api就够了。  
flask restful 的文档不难，很容易就看的懂，一些单词查查翻译，整个句子直白的很，很多文档都很容易懂。  
我想在开发完这个资源共享中心之后，继续开发的就是单词应用，用来学习英语，还有英文文档翻译。搜集网络上已有的翻译，整合起来。  
在之后的就是 rss 应用，用来聚合新闻，这个东西最关键的不在于数量，而在于质量，而且要有一定频率的更新。多了完全没有时间看。  

# 简单使用
引入 falsk，flask_restful
```python
from flask import Flask, request
from flask_restful import Resource, Api
```
实例化 api对象
```python
app = Flask(__name__)
api = Api(app)
```

Flask-RESTful从视图方法中解析多种类型的返回值。与Flask类似，可以返回任何可迭代的对象，它将被转换为响应，包括原始Flask响应对象。  
Flask-RESTful还支持使用多个返回值设置响应代码和响应头，最后返回的语句依次是 响应数据 响应码 响应头
```python
class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}
```




# 指定 falsk app 监听的地址和端口号
代码中指定，然后运行：`python **.py` 即可
```python
app.run(
    host = '0.0.0.0',
    port = 7777,  
    debug = True 
)
```
或者使用 flask 命令 ` falsk run -h 0.0.0.0 -p 7777`

# Request Parsing
## 请求参数解析
维护到2.0版本将会被废弃，可能用其他的包替代[marshmallow: simplified object serialization](https://marshmallow.readthedocs.io/en/3.0/)

请求解析接口`reqparse`由`argparse`接口二次开发而来，可以简便地访问`flask.request`里的任何变量
变量默认的类型为 unicode string
help参数值，在被返回错误时，作为错误信息
```python
from flask_restful import reqparse
# flask.Request.values dict 有两个值
parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')
args = parser.parse_args()
```

可以给解析的参数取别名
```python
parser.add_argument('name', dest='public_name')

args = parser.parse_args()
args['public_name']
```

RequestParser() 会解析 flask.Request.values, and flask.Request.json.
基本上请求的参数，无论 get,post,header,cookie,file 都能接收到，由 location 指定。
```python
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

# 解析多个位置
parser.add_argument('text', location=['headers', 'values'])

# 解析 json
parser.add_argument('language', type=list, location='json')
```

## Parser 继承
继承一个 Parser 对象，子类可以继承父类的请求参数，并且可以重写移除。

- `parser.copy()` 拷贝 parser对象
- `parser_copy.replace_argument()` 重写参数定义
- `parser_copy.remove_argument()` 移除参数定义

```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('foo', type=int)

parser_copy = parser.copy()
parser_copy.add_argument('bar', type=int)

# parser_copy has both 'foo' and 'bar'

parser_copy.replace_argument('foo', required=True, location='json')
# 'foo' is now a required str located in json, not an int as defined
#  by original parser

parser_copy.remove_argument('foo')
# parser_copy no longer has 'foo' argument
```

## Error 处理
处理请求错误，指定RequestParser选项参数`bundle_errors`
```python
from flask_restful import reqparse

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('foo', type=int, required=True)
parser.add_argument('bar', type=int, required=True)

# 如果请求没有都包含 `foo` `bar`参数，将会返回所有错误，默认的只会返回第一个参数错误，返回信息如下

{
    "message":  {
        "foo": "foo error message",
        "bar": "bar error message"
    }
}
```

为整个应用配置 请求错误处理
```python
from flask import Flask

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
```

每个字段的错误信息用`RequestParser.add_argument`的 `help` 参数指定
`help` 包含一个插值 `error_msg` , 表示错误类型的字符串
```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('foo', choices=('one', 'two'), help='Bad choice: {error_msg}')
# If a request comes in with a value of "three" for `foo`:
{
    "message":  {
        "foo": "Bad choice: three is not a valid choice",
    }
}
```


# 用 curl 发送请求
## 传送参数
```python
curl http://api.example.com -d "name=bob" -d "name=sue" -d "name=joe"
```
## 模拟各种类型的请求
```python
# GET请求
$ curl http://localhost:5000/todo1
{"todo1": "Remember the milk"}
# PUT请求
$ curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
{"todo1": "Remember the milk"}
# DELETE请求
$ curl http://localhost:5000/todos/todo2 -X DELETE -v
# post 请求
$ curl http://localhost:5000/todos -d "task=something new" -X POST -v
```

# Output Fields 输出字段
使用 fields 模型控制输出数据的结构
```python
from flask_restful import Resource, fields, marshal_with

resource_fields = {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822')
}

class Todo(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()

# marshal_with 装饰器的作用如下
class Todo(Resource):
    def get(self, **kwargs):
        return marshal(db_get_todo(), resource_fields), 200
```

给输出的字段重命名：
```python
fields = {
    'name': fields.String(attribute='private_name'),
    # lambda 函数
    'username': fields.String(attribute=lambda x: x._private_name),
    # 访问属性的属性
    'nickname': fields.String(attribute='people_list.0.person_dictionary.name'),
    # 设置默认值
    'firstname': fields.String(default='Anonymous User'),
    'address': fields.String,
}

```



## marshal_with 装饰器
使用 `marshal_with()` 装饰器 描述响应数据的格式
```python
from flask_restful import fields, marshal_with

resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')
```

# api接口多种输出格式
## json
使用标准库 json 模块，flask.json 序列化器包括JSON规范中没有的序列化功能。
```python
app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_reponse(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
```

## csv
```python
api = Api(app)

@api.representation('text/csv')
def output_csv(data, code, headers=None):
    pass
    # implement csv output!
```

## 多种输出类型
```python
class Api(restful.Api):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/xml': output_xml,
            'text/html': output_html,
            'text/csv': output_csv,
            'application/json': output_json,
        }
```

