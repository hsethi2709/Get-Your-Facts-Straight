from app import app
from flask import render_template,request, make_response,jsonify
import pymongo
import urllib
import predict as p1
import json
import copy

@app.route('/home')
def start():
    return render_template("start.html", title="Pre-Experiment Questionnaire")

@app.route('/post')
def end():
    return render_template("post.html", title="Post-Experiment Questionnaire")


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
    myrecord['experiments'] = {'1':{},'2':{},'3':{},'4':{}}
    if col.find_one(myrecord) is None:
        col.insert_one(myrecord)
    return {"status": 200}
   
@app.route("/sendFeedback", methods=['POST'])
def sendFeedback():
    client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
    db = client.afv
    col = db["participants"]
    requestJson = request.json
    cursor = col.find_one({'_id':requestJson['id'], "p_age": requestJson['p_age']})
    final = copy.deepcopy(cursor)
    level = str(requestJson['level'])
    final['experiments'][level][requestJson['sentence']] = {}
    final['experiments'][level][requestJson['sentence']]['feedback'] = requestJson['feedback_thumb'] 
    final["experiments"][level][requestJson['sentence']]['satisfaction_value'] = requestJson['satisfaction_value']
    if col.update(cursor, final, upsert=False):
        return {"status": 200}
    else:
        return {"status": 500}
