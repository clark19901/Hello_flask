from flask import abort  #处理错误
from flask import redirect #重定向
from flask_script import Manager  #可以使用命令行参数运行程序
from flask import Flask, render_template #Jinja2模板引擎
from flask_bootstrap import Bootstrap  #3b版本使用Flask-Bootstrap集成Twitter Bootstrap
from flask_moment import Moment   #使用Flask-Moment本地化日期和时间
from datetime import datetime
from flask import session,url_for
# url_for 函数使用URL 映射生成URL，从而保证URL 和定义的路由兼容，而且修改路由名字后
# 依然可用。
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
#，Flask-WTF 能保护所有表单免受跨站请求伪造（Cross-Site Request Forgery，
# CSRF）的攻击。恶意网站把请求发送到被攻击者已登录的其他网站时就会引发CSRF 攻击。
from flask import flash

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
# 实现CSRF 保护，Flask-WTF 需要程序设置一个密钥。Flask-WTF 使用这个密钥生成
# 加密令牌，再用令牌验证请求中表单数据的真伪

# <h1>Hello, World!</h1>
# <p> 当地时间是{{ moment(current_time).format('LLL') }}.</p>
# <p>这是在{{ moment(current_time).fromNow(refresh=True) }}</p>
# <p>{{current_time}}<p>

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')   #声明一个旧名提取自对话记录
        if old_name is not None and old_name != form.name.data:   #如果旧名和表单提交名不一样
            flash('Looks like you have changed your name!')       #需要同时在模板中渲染flash消息
        session['name'] = form.name.data
        return  redirect(url_for('index'))    #url_for唯一必须指定的参数是端点,即相应视图函数的名字
    return render_template('index.html', form=form,
                           name=session.get('name'),current_time= datetime.utcnow())

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