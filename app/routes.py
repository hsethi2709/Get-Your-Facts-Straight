from app import app
from flask import render_template,request, make_response,jsonify
import pymongo
import urllib
# import predict as p1
import json
import copy
import traceback

client = pymongo.MongoClient("mongodb+srv://hsethi2709:harshit2709@cluster0.wfcww.mongodb.net/afv?retryWrites=true&w=majority")
get_client = pymongo.MongoClient("mongodb+srv://hsethi2709:harshit2709@cluster0.wfcww.mongodb.net/afv?retryWrites=true&w=majority")
insert_client = pymongo.MongoClient("mongodb+srv://hsethi2709:harshit2709@cluster0.wfcww.mongodb.net/afv?retryWrites=true&w=majority")
insert_client_1 = pymongo.MongoClient("mongodb+srv://hsethi2709:harshit2709@cluster0.wfcww.mongodb.net/afv?retryWrites=true&w=majority")

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

@app.route('/feedback_1')
def feedback_1():
    return render_template("condition1_feedback.html", title="Questionnaire")

@app.route('/feedback_2')
def feedback_2():
    return render_template("condition2_feedback.html", title="Questionnaire")

@app.route('/feedback_3')
def feedback_3():
    return render_template("condition3_feedback.html", title="Questionnaire")

@app.route('/feedback_4')
def feedback_4():
    return render_template("condition4_feedback.html", title="Questionnaire")

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

@app.route("/dashboard_login")
def dashboard_login():
    return render_template("dashboard_login.html", title="Get Fact Check")

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
    db = get_client.afv
    myrecord = db['MasterList_Sentences_2']
    sentence_data = myrecord.find_one({"sentence":sentence})
    print(sentence_data)
    response = {}
    if data['level'] == 1:
        if sentence_data['ground_truth']:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = [sentence_data['supporting_evidence'][0]]
            response = claim_output
        else:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'REFUTES'
            claim_output['evidence'] = [sentence_data['refuting_evidence'][0]]
            response = claim_output
    elif data['level'] == 2 or data['level'] == 4:
        if sentence_data['ground_truth']:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = sentence_data['supporting_evidence']
            response = claim_output
        else:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'REFUTES'
            claim_output['evidence'] = sentence_data['refuting_evidence']
            response = claim_output
    elif data['level'] == 3:
        if sentence_data['ground_truth']:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'SUPPORTS'
            claim_output['SUPPORTS'] = [sentence_data['supporting_evidence'][0]]
            claim_output['REFUTES'] = sentence_data['supporting_evidence']
            response = claim_output
        else:
            claim_output = {}
            claim_output["claim"] = sentence
            claim_output['label'] = 'REFUTES'
            claim_output['SUPPORTS'] = sentence_data['supporting_evidence']
            claim_output['REFUTES'] = [sentence_data['refuting_evidence'][0]]
            response = claim_output
            
    # response = p1.predict_label(sentence, data['level'])
    res = jsonify(response)
    res.status_code = 200
    return res

@app.route('/addUser', methods=['POST'])
def addUser():
    
    db = insert_client.afv
    myrecord = request.json
    col = db['participants']
    myrecord['experiments'] = {'1':{},'2':{},'3':{},'4':{}}
    if col.find_one(myrecord) is None:
        col.insert_one(myrecord)
    return {"status": 200}
   
@app.route("/sendFeedback", methods=['POST'])
def sendFeedback():
    
    db = insert_client_1.afv
    col = db["participants_2"]
    requestJson = request.json
    cursor = col.find_one({'_id':int(requestJson['id'])})
    final = copy.deepcopy(cursor)
    level = str(requestJson['level'])
    final['experiments'][level][requestJson['sentence'][6:]] = {}
    final['experiments'][level][requestJson['sentence'][6:]]['trustScore'] = requestJson['trust_value'] 
    final["experiments"][level][requestJson['sentence'][6:]]['satisfaction_value'] = requestJson['satisfaction_value']
    if col.update(cursor, final, upsert=False):
        return {"status": 200}
    else:
        return {"status": 500}

@app.route("/addSentences", methods=['POST'])
def addSentences():
    
    db = insert_client.afv
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
    
    db = insert_client_1.afv
    collection = db['clientList_Sentences_2']
    requestJson = request.json
    cursor = collection.find_one({'_id': requestJson['pid']})
    if requestJson['stage'] == 'pre':
        if cursor == None:
            final = {
                    "_id":requestJson['pid'],
                    "pre":{requestJson['sentence_id'] : {"sentence":requestJson['sentence'],"label": requestJson['label'], "unaware": requestJson['unaware'], "confidence_scale": requestJson['confidence_scale']}}
                    }
            if collection.insert_one(final):
                return "Inserted Successfully"
            else:
                return "Insertion Failed"
        else:
            final = copy.deepcopy(cursor)
            final['pre'][requestJson['sentence_id']] = {"sentence":requestJson['sentence'],"label":requestJson['label'], "unaware": requestJson['unaware'], "confidence_scale":requestJson['confidence_scale']}
            if collection.update(cursor, final, upsert=False):
                return {'status':200}
            else:
                return {'status': 500}
    elif requestJson['stage'] == 'post':

            final = copy.deepcopy(cursor)
            if "post" not in final:
                final['post'] = {}
            final['post'][requestJson['sentence_id']] = {"sentence":requestJson['sentence'],"label":requestJson['label'], "confidence_scale": requestJson['confidence_scale']}
            if collection.update(cursor, final, upsert=False):
                return {'status':200}
            else:
                return {'status': 500}

@app.route("/readClientSentences", methods=['POST'])
def readSentences():
    
    db = get_client.afv
    collection = db['clientList_Sentences_2']
    requestJson = request.json
    cursor = collection.find_one({"_id":requestJson['pid']})
    if cursor == None:
        return "Error"
    else:
        sentences = []
        for sentence in cursor['pre']:
            sentences.append(cursor['pre'][sentence]['sentence'])
    
        return json.dumps(sentences)

@app.route("/readMasterSentences", methods=['GET'])
def readMasterSentence():
    try:
        
        db = get_client.afv
        collection = db['MasterList_Sentences_2']
        cursor = collection.find({},{"supporting_evidence":0,"refuting_evidence":0})
        if cursor == None:
            return "Error"
        else:
            return json.dumps(list(cursor))
    except Exception as e:
        return (e)

@app.route("/checkDuplicatePID", methods=['POST'])
def checkDuplicatePID():
    try:
        
        db = get_client.afv
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
        
        db = get_client.afv
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
        
        db = get_client.afv
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
        
        db = get_client.afv
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
        
        db = get_client.afv
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
        
        db = get_client.afv
        collection = db['clientList_Sentences']
        requestJson = request.json
        print(requestJson)
        cursor = collection.find_one({"_id": str(requestJson['pid'])})
        return {"participant_details": cursor}
    except Exception as e:
        return (e)

@app.route("/getSentenceAverageSatisfactionScore", methods=['POST'])
def getSentenceAverageSatisfactionScore():
    try:
        
        db = get_client.afv
        collection = db['participants']
        requestJson = request.json
        cursor = collection.find({})
        cursor = list(cursor)
        if cursor == None:
            return {'status': '500'}
        else:
            response = {}
            condition = requestJson['condition']
            count = 0
            for user in cursor:
                count += 1
                for sentence in user['experiments'][condition]:
                    if sentence not in response:
                        response[sentence] = {"trust": int(user['experiments'][condition][sentence]['trustScore']) ,"satisfaction": int(user['experiments'][condition][sentence]['satisfaction_value'])}
                    else:
                        response[sentence] = {"trust": (response[sentence]['trust']*(count-1) + int(user['experiments'][condition][sentence]['trustScore'])) / count,"satisfaction": (response[sentence]['satisfaction']*(count-1) + int(user['experiments'][condition][sentence]['satisfaction_value'])) / count}
            return response
    except Exception as e:
        return (e)

@app.route("/getTrueFakeData", methods=['GET'])
def getTrueFakeData():
    try:
        
        db = get_client.afv
        collection = db['clientList_Sentences']
        cursor = collection.find({})
        levels = ['1','2','3','4']
        true = 0
        fake = 0
        total = 0
        for user in cursor:
            print(user['_id'])
            for level in levels:
                if 'pre' in user[level]:
                    for sentence in user[level]['pre']:
                        if user[level]['pre'][sentence]['unaware'] == True:
                            total += 1
                            if user[level]['pre'][sentence]['label'] == 'True':
                                true += 1
                            elif user[level]['pre'][sentence]['label'] == 'Fake':
                                fake += 1
        true_per = (true/total) * 100
        return {"true": true_per}
    except Exception as e:
        print(traceback.print_exc())
        return (e)

@app.route("/checkPassword", methods=['POST'])
def checkPassword():
    requestJson = request.json
    print(requestJson)
    if requestJson['username'] == "dashboard@getfactcheck.me":
        if requestJson['password'] == "Unimelb-990198":
            return {"status":"True"}
        else:
            return {"status":"False"}
    else:
        return {"status":"False"}