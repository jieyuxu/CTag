from flask import Flask, render_template, request
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from utils.api import *
from utils.googleapi import *
from base64 import b64encode


app = Flask(__name__)
sess = flask_scoped_session(session_factory, app)

@app.route('/')
@app.route('/index.html')
def index():
    netid = "sukiy"
    user_obj = add_add_user(netid)
    album_obj= add_get_album("HELLO WORLD", user_obj)
    new_obj= add_get_album("little red", user_obj)

    with open("photo.jpeg", "rb") as image:
      f = base64.b64encode(image.read())

    img1 = Images(album=album_obj, picture=f)
    change_album(img1, new_obj)


    test = images_album(album_obj)
    return render_template("index.html")

# add images
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
            img_obj = add_image(bytes, album_obj, tags, d_types)

            type_tags = img_tags_all_category(img_obj)
            file_tag[f] = type_tags

        return render_template("success.html", album = album, file_tag = file_tag)

@app.route('/all_tags')
def all_tags():
    tags = get_all_tags()
    return render_template("all_tags.html", tags = tags)

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        if search is '':
            return render_template("index.html")
        input = search.split(',')
        tags = {}
        albums = []
        reject = []
        for i in input:
            i = i.strip()
            t = False
            a = False
            if is_tag(i):
                tags[i] = tag_num_img(i)
                t = True
            if is_album(i):
                albums.append(i)
                a = True
            if not a and not t:
                reject.append(i)
        return render_template("search.html", search=search, tags=tags,
                                              albums=albums, reject=reject)

@app.route('/image')
def image():
    id = request.args.get('img')
    img_obj = img_obj_id(id)
    album = album_obj_id(img_obj.album_id)
    type_tags = img_tags_all_category(img_obj)
    return render_template("image.html", image = image, album = album, type_tags = type_tags)

@app.route('/tag')
def tag():
    tag_name = request.args.get('tag_name')
    images = search_by_tag(tag_name)
    return render_template("tag.html", search = tag_name, images = images)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug = True)
