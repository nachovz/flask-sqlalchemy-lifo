import os
import sqlalchemy
from flask import Flask, jsonify, request
from models import db, Item
from flask_migrate import Migrate
from sqlalchemy import desc

app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/lifo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)


@app.route('/')
def hello():
    items = Item.query.all()
    response = []
    for i in items:
        response.append("%s" % i)
    
    return jsonify(response)











   
@app.route('/add', methods=['POST'])
def add():
    info = request.get_json() or {}
    item = Item(text=info["elephant"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})












@app.route('/lifo-pop', methods=['GET'])
def pop():
    last = Item.query.order_by(desc(Item.created_on)).first()
    if last is not None:
        db.session.delete(last)
        db.session.commit()
    return jsonify({ "deleted": "%s" % last })









@app.route('/fifo-pop', methods=['GET'])
def popFifo():
    last = Item.query.order_by(Item.created_on).first()
    if last is not None:
        db.session.delete(last)
        db.session.commit()
    return jsonify({ "deleted": "%s" % last })

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))