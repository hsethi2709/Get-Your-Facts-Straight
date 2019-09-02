from Flask import app
from flask import request, make_response,jsonify
from . import predict as p1

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    print(request.args.get('sentence'))
    sentence = request.args.get('sentence')
    #response = p1.predict_label(sentence)
    res = make_response(jsonify("{message:"+"sentence}"),200)
    return res
