from flask import Flask, render_template, request
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from utils.api import *
from utils.googleapi import *

app = Flask(__name__)
sess = flask_scoped_session(session_factory, app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
    netid = "sukiy"
    user_obj = add_add_user(netid)
    if request.method == 'POST':
        album = "little red"
        album_obj= add_get_album(album, user_obj)

        files = request.files.getlist("files[]")
        file_tag = {}
        for f in files:
            bytes = f.read()
            tags, types = annotate_img_bytestream(bytes)
            image = add_image(bytes, album_obj, tags, types)
            file_tag[f] = tags

        return render_template("success.html", file_tag = file_tag)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
