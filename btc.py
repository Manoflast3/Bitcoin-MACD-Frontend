# coding=utf-8
from flask import Flask, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy

# Env
PASSWORD = '123'

# Database Start #
app = Flask(__name__, static_url_path='')  # MySQL上线时记得改路径 还有127.0.0.1
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@119.29.8.78:3306/mytest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Record(db.Model):
    __tablename__ = 'trade_record'

    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.String(30))
    flag = db.Column(db.String(10))
    btnum = db.Column(db.String(20))
    price = db.Column(db.String(20))
    balance = db.Column(db.String(20))

    def __repr__(self):
        return '<Record %r>' % self.id

    def to_dict(self):
        return {
            "id": str(self.id),
            "date": self.date,
            "flag": self.flag,
            "btnum": self.btnum,
            "price": self.price,
            "balance": self.balance,
        }

# Database END #


# WEB Route and View Start #


@app.route('/')  # 主页直接返回静态页面
def index():
    return app.send_static_file("index.html")


@app.route('/<path:path>')  # 静态前端路径、带上线再换用NGINX处理
def Static_Route(path):
    return send_from_directory('/static', path)


@app.route('/record')  # 此部分用于查询交易记录
def Trade_Record():
    return jsonify({"data": [item.to_dict() for item in Record.query.all()]})


@app.route('/request', methods=['GET', 'POST'])  # 处理请求 响应post|get请求，并且校验密码是否符合，再执行action
def Action():
    if request.method == 'GET':
        if request.values.get("password") == PASSWORD:
            action = request.values.get("action")

            # 在这里写控制代码 要求有开始&倒计时24h 、 调试用的结束、

            return "request success"+action
        else:
            return "PassWord Err"
    else:
        return "POST Only"


# WEB Route and View END #

if __name__ == '__main__':
    app.run(debug=True)
