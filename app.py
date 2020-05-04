from flask import Flask, render_template, request, send_file, redirect
from flask import session, Response, make_response
from flask_sqlalchemy_session import flask_scoped_session
from utils.base import session_factory
from utils.api import *
from utils.googleapi import *
from utils.custom import *
from utils.get_image_feature_vectors import *
from utils.cluster_image_feature_vectors import *
from base64 import b64encode
from CAS import CAS, login
from CAS import login_required
from s3 import list_files, upload_file, check_file_bytes
from werkzeug.utils import secure_filename
from pdfkit import from_string, configuration
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'bdfa8a83f16eb4f95dc2473fe4a50820b14e74cc70cef6ae'
sess = flask_scoped_session(session_factory, app)

########## CAS AUTHENTICATION ###########
cas = CAS(app)
app.config['CAS_SERVER'] = "https://fed.princeton.edu/cas/login"
app.config['CAS_AFTER_LOGIN'] = 'caslogin'
# app.config['CAS_AFTER_LOGOUT'] = 'http://localhost:8000/caslogout'
app.config['CAS_AFTER_LOGOUT'] = 'http://ctagging.herokuapp.com//caslogout'
app.config['CAS_LOGIN_ROUTE'] = '/cas'
################# AWS ####################
UPLOAD_FOLDER = "uploads"
BUCKET = "iw-spring"

def isLoggedIn():
    if 'username' in session:
        return True
    return False

@app.route('/')
@app.route('/signin')
def signin():
    if isLoggedIn():
      albums = get_all_albums(session['username'])
      return render_template("index.html", albums=albums)
    return render_template("signin.html")

@app.route('/caslogin')
def caslogin():
   print(app.config['CAS_USERNAME_SESSION_KEY'])
   if cas.username is not None:
      print("user:", cas.username)
      session['username'] = cas.username
      print("confirming user logged into session", session['username'])
      session.modified = True
      add_get_user(cas.username)
   return redirect('/')

@app.route('/caslogout')
def caslogout():
   if isLoggedIn():
      session.pop('username')
      if 'admin' in session:
          session.pop('admin')
      session.modified = True
   return render_template("signin.html")

@app.route('/index')
def index():
  if isLoggedIn():
      albums = get_all_albums(session['username'])
      return render_template("index.html", albums=albums, user=session['username'])
  return render_template("signin.html")

# add images
@app.route('/success', methods = ['POST'])
def success():
    if isLoggedIn():
        # netid = "jyxu"
        user_obj = add_get_user(session['username'])
        non_valid = []
        if request.method == 'POST':
            album = request.form['a_name']
            album_obj= add_get_album(album, user_obj)

            files = request.files.getlist("file")
            file_tag = {}

            for f in files:
                # upload file to aws
                f.save(f.filename)
                if check_file_bytes(f.filename) == 0:
                    non_valid.append(f.filename)
                    continue
                upload_file(f"{f.filename}", BUCKET)
                link = "https://iw-spring.s3.amazonaws.com/uploads/%s" % f.filename

                f.seek(0)
                content = f.read()
                tags, d_types = annotate_img_bytestream(content)

                # gtags, d_types = annotate_img_bytestream(content)
                # custom_tags = custom_tagger(content)
                # tags, d_types = combine_tags(gtags, d_types, custom_tags)
                img_obj = add_image(album_obj, link, tags, d_types)

                type_tags = img_tags_all_category(img_obj)
                file_tag[f] = type_tags

                os.remove(f.filename)
            return render_template("success.html", album = album, file_tag = file_tag, non_valid = non_valid)
    return render_template("signin.html")

@app.route('/all_tags')
def all_tags():
    if isLoggedIn():
        tags = get_all_tags(session['username'])
        return render_template("all_tags.html", tags = tags, remove = False)
    return render_template("signin.html")

@app.route('/del_tags', methods=['POST', 'GET'])
def del_tags():
    if isLoggedIn():
        if request.method == 'POST':
            netid = session['username']
            # deleting
            del_tags = request.form.getlist('del_tags')
            remove = delete_perm_tags(del_tags, netid)

            # rendering
            tags = get_all_tags(netid)
            return render_template("all_tags.html", tags = tags, remove = remove)
    return render_template("signin.html")

@app.route('/search', methods = ['POST'])
def search():
    if isLoggedIn():
        if request.method == 'POST':
            search = request.form['search']
            if search is '':
                return render_template("index.html")
            netid = session['username']
            input = search.split(',')
            tags = {}
            albums = {}
            reject = []
            for i in input:
                i = i.strip().lower()
                t = False
                a = False
                num_images = len(search_by_tag(i, netid))
                if num_images != 0:
                    tags[i] = num_images
                    t = True
                results = get_search_albums(i, netid)
                if len(results) != 0:
                    for r in results:
                        num_images = len(images_album(r))
                        albums[r] = num_images
                    a = True
                if not a and not t:
                    reject.append(i)
            return render_template("search.html", search=search, tags=tags,
                                              albums=albums, reject=reject)
    return render_template("signin.html")

@app.route('/image')
def image():
    if isLoggedIn():
        id = request.args.get('img')
        img_obj = img_obj_id(id)
        album = album_obj_id(img_obj.album_id)
        type_tags = img_tags_all_category(img_obj)
        netid = session['username']
        choose_albums = all_albums_ns(netid)
        print(choose_albums)
        print(album)

        print(img_obj.url)

        similar_images = detect_web_uri(requests.get(img_obj.url).content)

        query = os.path.basename(img_obj.url)
        url_list= get_all_urls(img_obj.album_id)
        get_image_feature_vectors(url_list)
        nearest_neighbors = cluster(query)
        print(nearest_neighbors)

        try:
            del choose_albums[album]
        except:
            pass
        return render_template("image.html", id=id, image = img_obj.url, album = album,
                                type_tags = type_tags, choose_albums = choose_albums,
                                similar_images=similar_images, nearest_neighbors=nearest_neighbors)
    return render_template("signin.html")

@app.route('/delete_img', methods=['POST', 'GET'])
def delete_img():
    if isLoggedIn():
        if request.method == 'POST':
            a_id = request.form['a_id']
            img_obj = img_obj_id(request.form['img_id'])
            remove = False
            if img_obj is not None:
                remove_img(img_obj, a_id)
                remove = True
            album_obj = album_obj_id(a_id)
            if album_obj is None:
                netid = session['username']
                albums = get_all_albums(netid)
                return render_template('all_albums.html', albums = albums, remove = True,
                                                        change = False, a_change = '')
            images = images_album(album_obj)
            size = int(len(images) / 4)
            return render_template('album.html', images = images,
                                    album = album_obj, size = size, remove = remove,
                                    change = False, a_change = '')
    else:
        return render_template("signin.html")

@app.route('/edit_img_tag', methods=['POST', 'GET'])
def edit_img_tag():
    if isLoggedIn():
        if request.method == 'POST':
            id = request.form['img_id']
            img_obj = img_obj_id(id)
            album = album_obj_id(img_obj.album_id)
            # actual deleting
            del_tags = request.form.getlist('del_tags')
            tags = []
            for t in del_tags:
                tag_obj = get_tag_img(img_obj, t)
                tags.append(tag_obj)
            try:
                delete_tags(img_obj, tags)
            except:
                pass

            # adding tags
            add_tags = request.form['add_tags']
            if add_tags != '':
                tags = add_tags.split(',')
                type_obj = add_get_tagType('Custom Added')
                for t in tags:
                    tag_obj = add_get_tag(t.strip(), 100, type_obj)
                    add_tag_img(img_obj, tag_obj)

            # rendering
            type_tags = img_tags_all_category(img_obj)
            netid = session['username']
            choose_albums = all_albums_ns(netid)

            similar_images = detect_web_uri(requests.get(img_obj.url).content)

            query = os.path.basename(img_obj.url)
            url_list= get_all_urls(img_obj.album_id)
            get_image_feature_vectors(url_list)
            nearest_neighbors = cluster(query)
            print(nearest_neighbors)

            try:
                del choose_albums[album]
            except:
                pass
            return render_template("image.html", id=id, image = img_obj.url, album = album,
                                    type_tags = type_tags, choose_albums = choose_albums,
                                    similar_images=similar_images, nearest_neighbors=nearest_neighbors)
    return render_template("signin.html")

@app.route('/tag')
def tag():
    if isLoggedIn():
        tag_name = request.args.get('tag_name')
        images = search_by_tag(tag_name, session['username'])
        size = int(len(images) / 4)
        return render_template("tag.html", search = tag_name, images = images, size=size)
    return render_template("signin.html")

@app.route('/download/output.pdf', methods=['POST', 'GET'])
def download_pdf():
    if isLoggedIn():
        if request.method == 'POST':
            id = request.form['id']
            img_obj = img_obj_id(id)
            album = album_obj_id(img_obj.album_id)
            type_tags = img_tags_all_category(img_obj)

            config = configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')

            template_string = render_template("report.html", image = img_obj.url, album = album, type_tags = type_tags)

            response = make_response(from_string(template_string, False, configuration = config))
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

            # return send_file('output.pdf', as_attachment=True)
            return response
    else:
        return render_template("signin.html")

@app.route('/album')
def album():
    if isLoggedIn():
        album_id = request.args.get('id')
        album_obj = album_obj_id(album_id)
        images = images_album(album_obj)
        size = int(len(images) / 4)
        return render_template('album.html', images = images,
                                album = album_obj, size = size, remove = False, change = False)
    else:
        return render_template("signin.html")

@app.route('/album_imgs_del', methods=['POST', 'GET'])
def album_imgs_del():
    if isLoggedIn():
        a_id = request.form['id']
        album_obj = album_obj_id(a_id)
        images = images_album(album_obj)
        remove = False
        for i in images:
            id = str(i.image_id)
            try:
                if 'on' == request.form[id]:
                    remove_img(i, a_id)
                    remove = True
            except:
                pass

        album_obj = album_obj_id(a_id)
        if album_obj is None:
            albums = get_all_albums(session['username'])
            return render_template('all_albums.html', albums = albums, remove = True,
                                                    change = False, a_change = '')
        images = images_album(album_obj)
        size = int(len(images) / 4)
        return render_template('album.html', images = images,
                                album = album_obj, size = size, remove = remove, change = False)
    else:
        return render_template("signin.html")

@app.route('/change_album', methods=['POST', 'GET'])
def album_change():
    if isLoggedIn():
        if request.method == 'POST':
            # change album
            change = request.form['album_change']
            img_obj = img_obj_id(request.form['img_id'])
            user_obj = add_get_user(session['username'])
            if change == 'New Album':
                new = request.form['new_album']
                if new == '':
                    new = "[No Name]"
                new_album_obj = add_get_album(new, user_obj)
            else:
                new_album_obj = add_get_album(change, user_obj)

            change_album(img_obj, new_album_obj)

            # render album page
            album_id = request.form['a_id']
            album_obj = album_obj_id(request.form['a_id'])
            if album_obj is None:
                netid = session['username']
                albums = get_all_albums(netid)
                return render_template('all_albums.html', albums = albums, remove = False,
                                        change = True, a_change = new_album_obj.name)
            images = images_album(album_obj)
            size = int(len(images) / 4)
            return render_template('album.html', images = images, album = album_obj,
                                    size = size, remove = False, change = True,
                                    a_change = new_album_obj.name)
    else:
        return render_template("signin.html")

@app.route('/del_album', methods=['POST', 'GET'])
def del_album():
    if isLoggedIn():
        if request.method == 'POST':
            album_obj = album_obj_id(request.form['id'])
            remove = False
            if album_obj is not None:
                delete_album(album_obj)
                remove = True
            netid = session['username']
            albums = get_all_albums(netid)
            return render_template('all_albums.html', albums = albums, remove = remove,
                                                    change = False, a_change = '')
    else:
        return render_template("signin.html")

@app.route('/all_albums')
def all_albums():
    if isLoggedIn():
        netid = session['username']
        albums = get_all_albums(netid)
        return render_template('all_albums.html', albums = albums, remove = False, change = False)
    else:
        return render_template("signin.html")

@app.route('/rename_album', methods=['POST', 'GET'])
def rename_album():
    if isLoggedIn():
        album_obj = album_obj_id(request.form['id'])
        new_name = request.form['new_name']
        album_rename(album_obj, new_name)
        images = images_album(album_obj)
        size = int(len(images) / 4)
        return render_template('album.html', images = images,
                                album = album_obj, size = size, remove = False,
                                change = False, a_change = '')
    else:
        return render_template("signin.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug = True)
