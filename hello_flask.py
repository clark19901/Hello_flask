from flask import abort  #处理错误
from flask import redirect #重定向
from flask_script import Manager  #可以在运行时使用命令行
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
import  os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell  #让Flask-Script 的shell 命令自动导入特定的对象。区分Shell 大小写
from flask_migrate import Migrate, MigrateCommand #使用Flask-Migrate实现数据库迁移


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
#配置数据库
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
    users = db.relationship('User', backref='role')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #添加到User 模型中的role_id 列被定义为外键

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

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
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        old_name = session.get('name')   #声明一个旧名提取自对话记录
        if old_name is not None and old_name != form.name.data:   #如果旧名和表单提交名不一样
            flash('Looks like you have changed your name!')       #需要同时在模板中渲染flash消息
        return  redirect(url_for('index'))    #url_for唯一必须指定的参数是端点,即相应视图函数的名字
    return render_template('index.html', form=form,known=session.get('known', False),
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
    # app.run()  #host='192.168.0.100'
    manager.run()