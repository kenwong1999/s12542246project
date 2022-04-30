import hashlib
import time

from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from settings import Config


exe_id = hashlib.sha256(str(int(time.time() * 1000)).encode("utf-8")).hexdigest()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + Config.SQLITE_DIR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    lock = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/query", methods=['GET'])
def query():
    """
    Query products
    :return:
    """
    args = request.args.to_dict()
    product_id = args.get('id')
    if not product_id:
        return jsonify({'code': 400, 'msg': 'Missing parameter: product ID', 'exe_id': exe_id})

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({'code': 400, 'msg': 'Please input in the correct product ID', 'exe_id': exe_id})

    product = Product.query.get(product_id)
    if product:
        data = {}
        for k, v in product.__dict__.items():
            if k == '_sa_instance_state':
                continue
            data[k] = v
        return jsonify({'code': 200, 'msg': 'Query was successful', 'exe_id': exe_id, 'data': data})
    else:
        return jsonify({'code': 404, 'msg': 'Product ID does not exist', 'exe_id': exe_id})


@app.route('/buy', methods=['GET'])
def buy():
    """
    Buy some product
    :return:
    """
    required_arg = {'id', 'count', 'credit_card'}
    args = request.args.to_dict()

    # Validation of necessary parameter
    difference_set = required_arg - set(list(args.keys()))
    if difference_set:
        return jsonify({'code': 400, 'msg': f'Missing required parameters: {",".join(list(difference_set))}', 'exe_id': exe_id})

    product_id = args.get('id')
    try:
        count = int(args.get('count'))
    except ValueError:
        return jsonify({'code': 400, 'msg': 'Please input the quantity you want to buy correctly', 'exe_id': exe_id})
    credit_card = args.get('credit_card')

    # Validation of credit card account number
    if (len(credit_card) != 16) or (not (credit_card.isdigit())):
        return jsonify({'code': 400, 'msg': 'Please input in the correct credit-card number!', 'exe_id': exe_id})

    # Query inventory
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': 'Product ID does not exist', 'exe_id': exe_id})

    # Check lock
    while product.lock == 'true':
        product = Product.query.get(product_id)
        time.sleep(1)

    product.lock = 'true'
    db.session.commit()

    stock = product.quantity
    if stock >= count:

        product.quantity = stock - count
        product.lock = 'false'
        db.session.commit()

        return jsonify({'code': 200, 'msg': f'Buying {product.name},count：{count}，cost: {product.unit_price*count} RMB', 'exe_id': exe_id})
    else:
        product.lock = 'false'
        db.session.commit()
        return jsonify({'code': 200, 'msg': f'Product [{product.name}] out of storage!', 'exe_id': exe_id})


@app.route('/replenish', methods=['GET'])
def replenish():
    """
    Replenish product stock
    :return:
    """
    args = request.args.to_dict()
    product_id = args.get('id')

    if not product_id:
        return jsonify({'code': 400, 'msg': 'Please input in the correct product ID', 'exe_id': exe_id})

    try:
        int(product_id)
    except ValueError:
        return jsonify({'code': 400, 'msg': 'Please input in the correct product ID', 'exe_id': exe_id})

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': 'Product ID does not exist', 'exe_id': exe_id})

    try:
        count = int(args.get('count'))
    except ValueError:
        return jsonify({'code': 400, 'msg': 'Please input the correct inventory quantity', 'exe_id': exe_id})

    product.quantity += count
    db.session.commit()

    return jsonify({'code': 200, 'msg': f'Product [{product.name}] stock updates successful，current stock: {product.quantity}', 'exe_id': exe_id})


if __name__ == '__main__':
    app.run()



