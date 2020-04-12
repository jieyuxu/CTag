from utils.database import *
from flask_sqlalchemy_session import current_session
from sqlalchemy import and_
import base64

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
            tag_obj = add_get_tag(t, tags[t],type_obj)
            image.tags.append(tag_obj)

    sess.add(image)
    sess.commit()
    return image

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
def search_by_tag(tag_name):
    tags = sess.query(Tags)\
                .filter(Tags.name == tag_name)\
                .order_by(Tags.confidence.desc())\
                .all()
    if len(tags) == 0:
        return None
    for t in tags:
        images = sess.query(Image_Tags)\
                     .filter(Image_Tags.tag_id == t.tag_id)\
                     .all()
    match_images = imgtg_to_img(images)
    dict = {}
    for m in match_images:
        dict[m] = get_confidence(m, tag_name)
    return dict

############################################################## other functions #

# get all tag types for an image
def get_types_img(img_obj):
    tags = get_tags_general(img_obj)
    tag_types = []
    for t in tags:
        if t.tag_type not in tag_types:
            tag_types.append(t.tag_type)
    return tag_types

# get album by id
def album_obj_id(id):
    album = sess.query(Albums)\
                .filter(Albums.album_id == id)\
                .first()
    return album

# change album of an image
def change_album(image_obj, new_album_obj):
    image_obj.album = new_album_obj
    sess.commit()

# get image objs in album
def images_album(album_obj):
    images = sess.query(Images)\
                .filter(Images.album == album_obj)\
                .all()
    return images

# num of images with tag
def tag_num_img(name):
    search = sess.query(Tags)\
                .filter(Tags.name == name)\
                .all()
    for t in search:
        images = sess.query(Image_Tags)\
                     .filter(Image_Tags.tag_id == t.tag_id)\
                     .all()
    match_images = imgtg_to_img(images)
    return len(match_images)

# get all tags and num of images that contains that tag
def get_all_tags():
    tags = {}
    objs = sess.query(Tags).all()
    for o in objs:
        name = o.name
        if name not in tags:
            tags[name] = tag_num_img(name)
    return sorted(tags.items(), key=lambda x: x[1], reverse=True)

def is_tag(tag_name):
    tags = sess.query(Tags)\
                .filter(Tags.name == tag_name)\
                .all()
    if len(tags) == 0:
        return False
    return True

def is_album(album_name):
    album = sess.query(Albums)\
                .filter(Albums.name == album_name)\
                .all()
    if len(album) == 0:
        return False
    return True

def get_all_albums(user):
    a = sess.query(Albums)\
            .filter(Albums.net_id == user)\
            .all()

    return a
