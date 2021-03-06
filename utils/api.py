from utils.database import *
from flask_sqlalchemy_session import current_session
from sqlalchemy import and_, func
import base64
import os

sess = current_session

# get user obj, add user with net-id if not already exist
def add_get_user(netid):
    user = sess.query(Users).filter(Users.net_id == netid).first()
    if user is None:
        user = Users(net_id=netid)
        sess.add(user)
        sess.commit()
    return user

# make album if not already exist
def add_get_album(title, user_obj):
    a = sess.query(Albums)\
            .filter(and_(Albums.name == title, Albums.net_id == user_obj.net_id))\
            .first()
    if a is None:
        a = Albums(name=title, user=user_obj)
        sess.add(a)
        sess.commit()
    return a

# make tag_type
def add_get_tagType(type):
    t = sess.query(Tag_Types).filter(Tag_Types.name == type).first()
    if t is None:
        t = Tag_Types(name=type)
        sess.add(t)
        sess.commit()
    return t

# make new tag if not already exist
def add_get_tag(tag, conf, type_obj):
    t = sess.query(Tags)\
            .filter(and_(Tags.name == tag, Tags.confidence == conf))\
            .first()
    if t is None:
        t = Tags(name=tag, confidence=conf, type=type_obj)
        sess.add(t)
        sess.commit()
    return t

# add image to db, tags is dict [tag:conf], tag type is dict [tag:type]
def add_image(album, url, tags=None, tag_type=None):
    image = Images(album=album, url=url)
    if tags is not None:
        for t in tags:
            type_obj = add_get_tagType(tag_type[t])
            tag_obj = add_get_tag(t.lower(), tags[t], type_obj)
            image.tags.append(tag_obj)

    sess.add(image)
    sess.commit()
    return image

def add_tag_img(img_obj, tag_obj):
    img_obj.tags.append(tag_obj)
    sess.commit()

######################################################## sorting and searching #

# from an image object, get all tags by desc confidence
def sortConfidence(tag_obj):
    return tag_obj.confidence

# from image, get tags: no categories
def get_tags_general(img_obj):
    img_tags = sess.query(Image_Tags)\
                 .filter(Image_Tags.image_id == img_obj.image_id)\
                 .all()
    tags = []
    for t in img_tags:
        tags.append(sess.query(Tags)\
                        .filter(Tags.tag_id == t.tag_id)
                        .first())
    tags = list(filter(None, tags))
    tags.sort(key=sortConfidence, reverse=True)
    return tags

# from image, get tags in one category
def img_tags_one_category(img_obj, type_obj):
    img_tags = sess.query(Image_Tags)\
                 .filter(Image_Tags.image_id == img_obj.image_id)\
                 .all()
    tags = []
    for t in img_tags:
        tags.append(sess.query(Tags)\
                        .filter(and_(Tags.tag_id == t.tag_id, Tags.tag_type == type_obj))
                        .first())
    tags = list(filter(None, tags))
    tags.sort(key=sortConfidence, reverse=True)
    return tags

# get all tag types for an image
def get_types_img(img_obj):
    tags = get_tags_general(img_obj)
    tag_types = []
    for t in tags:
        if t.tag_type not in tag_types:
            tag_types.append(t.tag_type)
    return tag_types

def img_tags_all_category(img_obj):
    types = get_types_img(img_obj) # all tag types in the image
    type_tags = {} # dict of all tags per type

    # sort tags by category by confidence
    for ty in types:
        tag_objs = img_tags_one_category(img_obj, ty)
        sorted_tags = []
        for t in tag_objs:
            sorted_tags.append([t.name, t.confidence])
        type_tags[ty] = sorted_tags

    return type_tags

# get img obj from img id
def img_obj_id(id):
    img = sess.query(Images)\
                .filter(Images.image_id == id)\
                .first()
    return img

# input array of image_tag objects, get array of image objects
def imgtg_to_img(array):
    images = []
    for i in array:
        images.append(img_obj_id(i.image_id))
    return images

# get confidence of img from tag_name
def get_confidence(img_obj, tag_name):
    tags = get_tags_general(img_obj)
    for t in tags:
        if t.name == tag_name:
            return t.confidence
    return 0

# get all images with tag name in descending get_confidence
# returns dict of image objects to confidence
def search_by_tag(tag_name, netid):
    print(tag_name)
    user_obj = add_get_user(netid)
    albums = all_albums_ns(netid)
    images = []
    for a in albums:
        img = images_album(a)
        for i in img:
            images.append(i)
    bingo = {}
    for i in images:
        flag = False
        iTags = img_tags_all_category(i)
        for types in iTags:
            for pair in iTags[types]:
                t = pair[0]
                confidence = pair[1]
                if t == tag_name:
                    bingo[i] = confidence
                    flag = True
                    break
            if flag == True:
                break
    return sorted(bingo.items(), key=lambda x: x[1], reverse=True)

####################################################################### albums #

# get album by id
def album_obj_id(id):
    album = sess.query(Albums)\
                .filter(Albums.album_id == id)\
                .first()
    return album

def check_album(album_obj):
    num = len(images_album(album_obj))
    if num == 0:
        sess.delete(album_obj)
    sess.commit()

# remove image from album
def remove_img(img_obj, album_id):
    # delete image obj and remove it from album
    sess.delete(img_obj)
    sess.commit()
    # check if album has anything
    album_obj = album_obj_id(album_id)
    check_album(album_obj)

# change album of an image
def change_album(image_obj, new_album_obj):
    old_album = image_obj.album
    image_obj.album = new_album_obj
    sess.commit()
    check_album(old_album)

# get image objs in album
def images_album(album_obj):
    images = sess.query(Images)\
                .filter(Images.album == album_obj)\
                .all()
    return images

# get all albums with same letters as album_name, regardless of case
def get_search_albums(album_name, netid):
    album = sess.query(Albums)\
                .filter(func.lower(Albums.name) == album_name, Albums.net_id == netid)\
                .all()
    return album

# sorted
def get_all_albums(user):
    albums = {}
    query = sess.query(Albums)\
            .filter(Albums.net_id == user)\
            .all()
    for q in query:
        albums[q] = len(images_album(q))
    return sorted(albums.items(), key=lambda x: x[1], reverse=True)

# not sorted
def all_albums_ns(netid):
    albums = {}
    query = sess.query(Albums)\
            .filter(Albums.net_id == netid)\
            .all()
    for q in query:
        albums[q] = len(images_album(q))
    return albums

def delete_album(album_obj):
    images = images_album(album_obj)
    for i in images:
        sess.delete(i)
    sess.delete(album_obj)
    sess.commit()

def album_rename(album_obj, new_name):
    album_obj.name = new_name
    sess.commit()

def get_all_urls(album_id):
    urls = []
    query = album_obj_id(album_id)

    images = images_album(query)

    for img_obj in images:
        urls.append(img_obj.url)

    return urls


####################################################################### others #

# get all tags and num of images that contains that tag
def get_all_tags(netid):
    user_obj = add_get_user(netid)
    albums = all_albums_ns(netid)
    tags = {}
    for a in albums:
        img = images_album(a)
        for i in img:
            iTags = get_tags_general(i)
            for t in iTags:
                if t.name == 'sorrow':
                    print('here')
                    print(i)
                t = t.name
                if t in tags:
                    tags[t] += 1
                else:
                    tags[t] = 1
    return sorted(tags.items(), key=lambda x: x[1], reverse=True)

# image size valid?
def check_size(content):
    TWENTY_MB = 20971520
    size = len(content)
    if (size == 0) or (size > TWENTY_MB):
        return False
    return True

# combine tags from coures
def combine_tags(gtags, d_types, custom_tags):
    google = set(gtags.keys())
    custom = set(custom_tags.keys())
    oGoogle = google.difference(custom)
    oCustom = custom.difference(google)
    tags = {}

    # for same ones
    for c in custom_tags:
        if c in gtags:
            custom = custom_tags[c] * 100
            print(custom)
            print(gtags[c])
            tags[c] = (custom + gtags[c]) / 2.0
    # those only in googleapis
    for c in oGoogle:
        tags[c] = gtags[c] / 2.0
    for c in oCustom:
        custom = custom_tags[c] * 100
        tags[c] = (custom / 2.0) 
        print(tags[c])
        d_types[c] = 'Label'

    return tags, d_types

# delete tag from image, array of tag_objs
# returns False if reload
def delete_tags(img_obj, tags):
    for tag_obj in tags:
        query = sess.query(Image_Tags)\
                    .filter(and_(Image_Tags.image_id == img_obj.image_id, Image_Tags.tag_id == tag_obj.tag_id))\
                    .first()
        sess.delete(query)
    sess.commit()
    return True

# array of tag names
def delete_perm_tags(tags, netid):
    # get images with the tag
    for tag_name in tags:
        imgs = search_by_tag(tag_name, netid)
        if len(imgs) == 0:
            return False
        for i in imgs:
            img_obj = i[0]
            tag_obj = get_tag_img(img_obj, tag_name)
            reload = delete_tags(img_obj, [tag_obj])
    sess.commit()
    return True


def get_tag_img(img_obj, tag_name):
    tags = get_tags_general(img_obj)
    for t in tags:
        if t.name == tag_name:
            return t
    return
