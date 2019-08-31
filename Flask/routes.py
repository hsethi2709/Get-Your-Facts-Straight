from Flask import app
from flask import request, make_response,jsonify

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    print(request.args.get('sentence'))
    sentence = request.args.get('sentence')
    res = make_response(jsonify({"message": "This is Fake"}),200)
    return res
