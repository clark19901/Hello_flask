from flask import Flask,render_template
from flask_mail import Mail,Message
from flask_script import Manager

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '822650822@qq.com'
app.config['MAIL_PASSWORD'] = 'ysbzeiqcjwxibajh'
mail = Mail(app)
@app.route('/')
def index():
    msg = Message('主题', sender='822650822@qq.com', recipients=['822650822@qq.com'])
    msg.body = '文本 body'
    msg.html = '<b>HTML</b> body'
    mail.send(msg)
    return "<h1>发送成功</h1>"

if __name__ == '__main__':
    app.run(debug=True)