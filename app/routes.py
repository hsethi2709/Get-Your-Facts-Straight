from app import app
from flask import render_template,request, make_response,jsonify
import pymongo
import urllib
import predict as p1
import json
import copy

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/pre')
def start():
    return render_template("start.html", title="Pre-Experiment Questionnaire")

@app.route('/post')
def end():
    return render_template("post.html", title="Post-Experiment Questionnaire")

@app.route("/login")
def login():
    return render_template("login.html", title="Get Fact Check")

@app.route("/home")
def home():
    return render_template("index.html", title="Get Fact Check")

@app.route("/training")
def train():
    return render_template("training.html", title="Get Fact Check")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html", title="Get Fact Check")

@app.route("/experiment")
def experiment():
    return render_template("experiment.html", title="Get Fact Check")

@app.route("/experimentInstruction")
def experimentInstruction():
    return render_template("experiment_instruction.html", title="Get Fact Check")

@app.route("/postExperimentInstruction")
def postExperimentInstruction():
    return render_template("post_experiment_instructions.html", title="Get Fact Check")

@app.route("/postExperiment")
def postExperiment():
    return render_template("postExperiment.html", title="Get Fact Check")

@app.route("/preExperiment")
def preExperiment():
    return render_template("preExperiment.html", title="Get Fact Check")

@app.route("/thankyou")
def thankYou():
    return render_template("thankyou.html", title="Get Fact Check")

@app.route("/dashboard.html")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Get Fact Check")

@app.route("/profile.html")
def profile():
    return render_template("profile.html", title="Get Fact Check")

@app.route("/table.html")
def table():
    return render_template("table.html", title="Get Fact Check")

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
    cursor = col.find_one({'_id':int(requestJson['id'])})
    final = copy.deepcopy(cursor)
    level = str(requestJson['level'])
    final['experiments'][level][requestJson['sentence']] = {}
    final['experiments'][level][requestJson['sentence']]['trustScore'] = requestJson['trust_value'] 
    final["experiments"][level][requestJson['sentence']]['satisfaction_value'] = requestJson['satisfaction_value']
    if col.update(cursor, final, upsert=False):
        return {"status": 200}
    else:
        return {"status": 500}

@app.route("/addSentences", methods=['POST'])
def addSentences():
    client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
    db = client.afv
    collection = db['MasterList_Sentences']
    requestJson = request.json
    cursor = collection.find_one({'_id': requestJson['level']})
    if cursor == None:
        final = {"_id": requestJson['level'], "Sentences": [requestJson['sentence']]}
        if collection.insert_one(final):
            return "Inserted Successfully"
        else:
            return "Insertion Failed"
    else:
        final = copy.deepcopy(cursor)
        final['Sentences'].append(requestJson['sentence'])
        if collection.update(cursor, final, upsert=False):
            return {"status": 200}
        else:
            return {"status": 500}

@app.route("/addSentenceToClient", methods=['POST'])
def addSentenceToClient():
    client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
    db = client.afv
    collection = db['clientList_Sentences']
    requestJson = request.json
    cursor = collection.find_one({'_id': requestJson['pid']})
    if requestJson['stage'] == 'pre':
        if cursor == None:
            final = {
                    "_id":requestJson['pid'],
                    requestJson['level']:{"pre":{requestJson['sentence'].replace('.','_') : {"label": requestJson['label'], "unaware": requestJson['unaware']}}}
                    }
            if collection.insert_one(final):
                return "Inserted Successfully"
            else:
                return "Insertion Failed"
        else:
            final = copy.deepcopy(cursor)
            if requestJson['level'] not in final:
                final[requestJson['level']] = {'pre':{}}
            final[requestJson['level']]['pre'][requestJson['sentence']] = {"label":requestJson['label'], "unaware": requestJson['unaware']}
            if collection.update(cursor, final, upsert=False):
                return {'status':200}
            else:
                return {'status': 500}
    elif requestJson['stage'] == 'post':

            final = copy.deepcopy(cursor)
            if requestJson['level'] not in final:
                final[requestJson['level']] = {'post':{}}
            if "post" not in final[requestJson['level']]:
                final[requestJson['level']]['post'] = {}
            final[requestJson['level']]['post'][requestJson['sentence']] = requestJson['label']
            if collection.update(cursor, final, upsert=False):
                return {'status':200}
            else:
                return {'status': 500}

@app.route("/readClientSentences", methods=['POST'])
def readSentences():
    client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
    db = client.afv
    collection = db['clientList_Sentences']
    requestJson = request.json
    cursor = collection.find_one({"_id":requestJson['pid']})
    if cursor == None:
        return "Error"
    else:
        sentences = []
        for sentence in cursor[requestJson['level']]['pre'].keys():
            sentences.append(sentence.replace('_','.'))
    
        return json.dumps(sentences)

@app.route("/readMasterSentences", methods=['POST'])
def readMasterSentence():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['MasterList_Sentences']
        requestJson = request.json
        cursor = collection.find_one({"_id": requestJson['level']})
        if cursor == None:
            return "Error"
        else:
            return json.dumps(cursor['Sentences'])
    except Exception as e:
        return (e)

@app.route("/checkDuplicatePID", methods=['POST'])
def checkDuplicatePID():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['participants']
        requestJson = request.json
        cursor = collection.find_one({"_id": requestJson['pid']})
        if cursor == None:
            return {'status': 'false'}
        else:
            return {'status': 'true'}
    except Exception as e:
        return (e)


# Dashboard API's

@app.route("/getTotalParticipants", methods=['GET'])
def getTotalPID():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['participants']
        cursor = collection.find({})
        if cursor == None:
            return {'status': '500'}
        else:
            count = 0
            for item in cursor:
                count += 1
            return {"count": count}
    except Exception as e:
        return (e)

@app.route("/getAverageTrustScore", methods=['GET'])
def getAverageTrustScore():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['participants']
        cursor = collection.find({})
        cursor = list(cursor)
        if cursor == None:
            return {'status': '500'}
        else:
            response = {}
            conditions = ["1","2","3","4"]
            for condition in conditions:
                print(condition)
                count = 0
                sum = 0
                for item in cursor:
                    for _,data in item['experiments'][condition].items():
                        sum += int(data['trustScore'])
                        count +=1
                average = sum / count
                print(average)
                response[condition] = average
            return response
    except Exception as e:
        return (e)

@app.route("/getAverageSatisfactionScore", methods=['GET'])
def getAverageSatisfactionScore():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['participants']
        cursor = collection.find({})
        cursor = list(cursor)
        if cursor == None:
            return {'status': '500'}
        else:
            response = {}
            conditions = ["1","2","3","4"]
            for condition in conditions:
                print(condition)
                count = 0
                sum = 0
                for item in cursor:
                    for _,data in item['experiments'][condition].items():
                        sum += int(data['satisfaction_value'])
                        count +=1
                average = sum / count
                print(average)
                response[condition] = average
            return response
    except Exception as e:
        return (e)

@app.route("/getListOfParticipants", methods=['GET'])
def getListofParticipants():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['participants']
        cursor = collection.find({})
        participantsList = []
        cursor = list(cursor)
        for item in cursor:
            participantsList.append(item['_id'])
        return {"participants": participantsList}
    except Exception as e:
        return e

@app.route("/getProfileInfo", methods=['POST'])
def getProfileInfo():
    try:
        client = pymongo.MongoClient("mongodb://harshit:" + urllib.parse.quote("harshit2709") + "@45.113.232.191/afv")
        db = client.afv
        collection = db['clientList_Sentences']
        requestJson = request.json
        print(requestJson)
        cursor = collection.find_one({"_id": str(requestJson['pid'])})
        return {"participant_details": cursor}
    except Exception as e:
        return (e)