
from flask import abort  #处理错误
from flask import redirect #重定向
from flask_script import Manager  #可以使用命令行参数运行程序
from flask import Flask, render_template #Jinja2模板引擎
from flask_bootstrap import Bootstrap  #3b版本使用Flask-Bootstrap集成Twitter Bootstrap
from flask_moment import Moment   #使用Flask-Moment本地化日期和时间
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# 代码示例 route() 装饰器把一个函数绑定到对应的 URL 上。
# @app.route('/')
# def index():
#     return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/re')
def redi():
    return redirect('http://www.baidu.com')
#重定向 告诉浏览器一个新地址用以加载新页面

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h1>Hello, %s</h1>' % user.name


@app.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

# 添加了一个动态路由。访问这个地址时，你会看到一则针对个人的欢迎消息。


# @app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, %s!</h1>' % name

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404   #客户端请求未知页面或路由时
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500   #有未处理的异常时




if __name__ == "__main__":
    app.debug = True
    # 启用了调试支持，服务器会在代码修改后自动重新载入 ，并在发生错误时提供一个相当有用的调试器 。
    app.run(host='192.168.0.100')