from utils.database import *
from flask_sqlalchemy_session import current_session
from os import listdir
import base64

sess = current_session

# input listdir of images
# get a list of all the corrupt image files
# If nothing prints out, all of those image files are good, valid images.
def detect_corrupt():
    for filename in listdir('./'):
        try:
          img = Image.open('./' + filename) # open the image file
          img.verify() # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
          print('Bad file:', filename) # print out the names of corrupt files

# input array of image_tag objects, get array of image objects
def imgtg_to_img(array):
    images = []
    for i in array:
        images.append(sess.query(Images)\
                            .filter(Images.image_id == i.image_id)
                            .first())
    return images

# get all images with tag name in descending confidence, returns image objects
def search_by_tag(tag_name):
    tags = sess.query(Tags)\
                .filter(Tags.name == tag_name)\
                .order_by(Tags.confidence.desc())\
                .all()
    for t in tags:
        images = sess.query(Image_Tags)\
                     .filter(Image_Tags.tag_id == t.tag_id)\
                     .all()
    return imgtg_to_img(images)

# from an image object, get all tags by order of confidence
def sortConfidence(tag_obj):
    return tag_obj.confidence

def get_tags(img_obj):
    img_tags = sess.query(Image_Tags)\
                 .filter(Image_Tags.image_id == img_obj.image_id)\
                 .all()
    tags = []
    for t in img_tags:
        tags.append(sess.query(Tags)\
                        .filter(Tags.tag_id == t.tag_id)
                        .first())
    tags.sort(key=sortConfidence, reverse=True)
    return tags

# add user with net-id
def add_user(netid):
    user = Users(net_id=netid)
    sess.add(user)
    sess.commit()
    return user

# make album, input user object
def add_album(title, user_obj):
    a = Albums(name=title, user=user_obj)
    sess.add(a)
    sess.commit()
    return a

# make tag_type
def add_tagType(type):
    t = Tag_Types(name=type)
    sess.add(t)
    sess.commit()
    return t

# make new tag
def add_tag(tag, conf, type_obj):
    t = Tags(name=tag, confidence=conf, type=type_obj)
    sess.add(t)
    sess.commit()
    return t

# add image to db, tags is an array of tag objects
def add_image(filename, album, tags=None):
    with open(filename, "rb") as image:
      f = base64.b64encode(image.read())

    image = Images(album=album, picture=f)
    if tags is not None:
        for t in tags:
            image.tags.append(t)

    sess.add(image)
    sess.commit()
    return image
