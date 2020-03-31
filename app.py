from flask import Flask, render_template, request
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from utils.api import *

app = Flask(__name__)
sess = flask_scoped_session(session_factory, app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        files = request.files.getlist("files[]")
        print(files)
        return render_template("success.html", files = files)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
