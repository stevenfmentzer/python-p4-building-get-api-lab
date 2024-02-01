#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    if bakeries: 
        dict_list = [bakery.to_dict() for bakery in bakeries]
        response = make_response(
            dict_list, 
            200)
    else: 
        response = make_response(
            "No bakeries found", 
            404)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery: 
        bakery_dict = bakery.to_dict()
        response = make_response(
            bakery_dict,
            200)
    else: 
        response = make_response(
            f"Bakery ID: {id} not found",
            404)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    if goods: 
        goods_dict = [good.to_dict() for good in goods]
        response = make_response(
            goods_dict, 
            200)
    else: 
        response = make_response(
            f"No baked goods were found", 
            404)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if good: 
        good_dict = good.to_dict()
        response = make_response(
            good_dict, 
            200)
    else: 
        response = make_response(
            f"No baked goods were found", 
            404)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
