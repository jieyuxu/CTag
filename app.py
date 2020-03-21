from flask import Flask, render_template
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from utils.api import *

app = Flask(__name__)
sess = flask_scoped_session(session_factory, app)

@app.route('/')
def index():
    images = search_by_tag('truck')
    return render_template("index.html", images = imges)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
