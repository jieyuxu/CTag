from flask import Flask, request, render_template, url_for, redirect, current_app, json, make_response
from flask import session, Response
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from CAS import CAS, login
from CAS import login_required
from utils.api import *

app = Flask(__name__)
sess = flask_scoped_session(session_factory, app)

@app.route('/')
def index():
    images = search_by_tag('truck')
    return render_template("index.html", images = images)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
