from app import app
from flask import request, make_response,jsonify
import predict as p1

@app.route('/')
@app.route('/index', methods=['POST','GET'])
def index():
    sentence = request.args.get('sentence')
    response = p1.predict_label(sentence)
    res = jsonify(response)
    res.status_code = 200
    return res
