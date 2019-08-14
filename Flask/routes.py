from Flask import app
from flask import request
@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    print(request.args.get('sentence'))
    sentence = request.args.get('sentence')
    return sentence
