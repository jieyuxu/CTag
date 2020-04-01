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
        album = request.form['a_name']
        album_obj= add_get_album(album, user_obj)

        files = request.files.getlist("files[]")
        file_tag = {}
        for f in files:
            # add image to db
            bytes = f.read()
            tags, d_types = annotate_img_bytestream(bytes)
            image = add_image(bytes, album_obj, tags, d_types)

            types = get_types_img(image) # all tag types in the image
            type_tags = {} # dict of all tags per type

            # sort tags by category by confidence
            for ty in types:
                tag_objs = get_tags_category(image, ty)
                sorted_tags = []
                for t in tag_objs:
                    sorted_tags.append([t.name, t.confidence])
                type_tags[ty] = sorted_tags
            file_tag[f] = type_tags

        return render_template("success.html", album = album, file_tag = file_tag)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
