from flask import Flask

app = Flask(__name__)

#代码示例 route() 装饰器把一个函数绑定到对应的 URL 上。
#@app.route('/')
# def index():
#     return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/')
def hello_world():
    return "<h1>Hello Wolrd!<h1>"

#添加了一个动态路由。访问这个地址时，你会看到一则针对个人的欢迎消息。
@app.route('/user/<name>')

def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == "__main__":
    app.debug = True
    # 启用了调试支持，服务器会在代码修改后自动重新载入 ，并在发生错误时提供一个相当有用的调试器 。
    app.run(host='192.168.0.100')
