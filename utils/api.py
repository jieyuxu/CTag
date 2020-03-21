from utils.database import Users, Albums, Images, Tags, Tag_Types, Image_Tags
from sqlalchemy import or_, and_
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

# for an image, get all tags by order of confidence

# # add image to db
# def add_image(filename):
#     with open(filename, "rb") as image:
#       f = base64.b64encode(image.read())
