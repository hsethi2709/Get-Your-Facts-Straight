from app import app
from flask import request, make_response,jsonify
import pymongo
import urllib
import predict as p1
import json

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    sentence = request.args.get('sentence')
    data = request.get_json()
    print(data)
    response = p1.predict_label(sentence, data['level'])
    res = jsonify(response)
    res.status_code = 200
    return res

@app.route('/addUser', methods=['POST'])
def addUser():
    client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
    db = client.afv
    myrecord = request.json
    col = db['participants']
    col.insert_one(myrecord)
    return {"status": 200}
    

