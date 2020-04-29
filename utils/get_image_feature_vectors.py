#################################################
# Imports and function definitions
#################################################
# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub

# For saving 'feature vectors' into a txt file
import numpy as np

# Time for measuring the process time
import time

# Glob for reading file names in a folder
import glob
import os.path

# read img from url
from PIL import Image 

# import requests
import requests
#################################################

#################################################
# This function:
# Loads the JPEG image at the given path
# Decodes the JPEG image to a uint8 W X H X 3 tensor
# Resizes the image to 224 x 224 x 3 tensor
# Returns the pre processed image as 224 x 224 x 3 tensor
#################################################
def load_img(path):

  # Reads the image file and returns data type of string
  img = tf.io.read_file(path)

  # read img from url instead

  # Decodes the image to W x H x 3 shape tensor with type of uint8
  img = tf.io.decode_jpeg(img, channels=3)

  # Resize the image to 224 x 244 x 3 shape tensor
  img = tf.image.resize_with_pad(img, 224, 224)

  # Converts the data type of uint8 to float32 by adding a new axis
  # This makes the img 1 x 224 x 224 x 3 tensor with the data type of float32
  # This is required for the mobilenet model we are using
  img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

  return img

def load_img_from_url(url):
    
  # Reads the image file and returns data type of string 
  # response = requests.get(url, stream=True)
  # img = Image.open(response.raw)
  # img = tf.io.read_file(path)

  # Decodes the image to W x H x 3 shape tensor with type of uint8
  img = tf.io.decode_jpeg(requests.get(url).content, channels=3)

  # Resize the image to 224 x 244 x 3 shape tensor
  img = tf.image.resize_with_pad(img, 224, 224)

  # Converts the data type of uint8 to float32 by adding a new axis
  # This makes the img 1 x 224 x 224 x 3 tensor with the data type of float32
  # This is required for the mobilenet model we are using
  img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

  return img

#################################################
# This function:
# Loads the mobilenet model in TF.HUB
# Makes an inference for all images stored in a local folder
# Saves each of the feature vectors in a file
#################################################
# def get_image_feature_vectors():

#   i = 0

#   start_time = time.time()

#   print("---------------------------------")
#   print ("Step.1 of 2 - mobilenet_v2_140_224 - Loading Started at %s" %time.ctime())
#   print("---------------------------------")

#   # Definition of module with using tfhub.dev handle
#   module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4" 
  
#   # Load the module
#   module = hub.load(module_handle)

#   print("---------------------------------")
#   print ("Step.1 of 2 - mobilenet_v2_140_224 - Loading Completed at %s" %time.ctime())
#   print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))

#   print("---------------------------------")
#   print ("Step.2 of 2 - Generating Feature Vectors -  Started at %s" %time.ctime())
 

#   # Loops through all images in a local folder
#   for filename in glob.glob('/Users/amy/Documents/IW_JuniorSpring/training/images/s9/*'): #assuming gif
#     i = i + 1

#     print("-----------------------------------------------------------------------------------------")
#     print("Image count                     :%s" %i)
#     print("Image in process is             :%s" %filename)

#     # Loads and pre-process the image
#     img = load_img(filename)

#     # Calculate the image feature vector of the img
#     features = module(img)   
  
#     # Remove single-dimensional entries from the 'features' array
#     feature_set = np.squeeze(features)  

#     # Saves the image feature vectors into a file for later use

#     outfile_name = os.path.basename(filename).split('.')[0] + ".npz"
#     out_path = os.path.join('/Users/amy/Documents/IW_JuniorSpring/ImageSimilarityDetection/feature-vectors/', outfile_name)

#     # Saves the 'feature_set' to a text file
#     np.savetxt(out_path, feature_set, delimiter=',')

#     print("Image feature vector saved to   :%s" %out_path)
  
#   print("---------------------------------")
#   print ("Step.2 of 2 - Generating Feature Vectors - Completed at %s" %time.ctime())
#   print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))
#   print("--- %s images processed ---------" %i)

def get_image_feature_vectors(url_list):
    
  i = 0

  start_time = time.time()

  print("---------------------------------")
  print ("Step.1 of 2 - mobilenet_v2_140_224 - Loading Started at %s" %time.ctime())
  print("---------------------------------")

  # Definition of module with using tfhub.dev handle
  module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4" 
  
  # Load the module
  module = hub.load(module_handle)

  print("---------------------------------")
  print ("Step.1 of 2 - mobilenet_v2_140_224 - Loading Completed at %s" %time.ctime())
  print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))

  print("---------------------------------")
  print ("Step.2 of 2 - Generating Feature Vectors -  Started at %s" %time.ctime())
 

  # Loops through all images in a local folder
  for url in url_list:
    i = i + 1

    print("-----------------------------------------------------------------------------------------")
    print("Image count                     :%s" %i)
    print("Image in process is             :%s" %url)

    # Loads and pre-process the image
    img = load_img_from_url(url)

    # Calculate the image feature vector of the img
    features = module(img)   
  
    # Remove single-dimensional entries from the 'features' array
    feature_set = np.squeeze(features)  

    # Saves the image feature vectors into a file for later use
    print(os.path.basename(url).split('.'))
    print(os.path.basename(url))
    outfile_name = os.path.basename(url) + ".npz"
    out_path = os.path.join('/app/vector-features', outfile_name)

    # Saves the 'feature_set' to a text file
    np.savetxt(out_path, feature_set, delimiter=',')

    print("Image feature vector saved to   :%s" %out_path)
  
  print("---------------------------------")
  print ("Step.2 of 2 - Generating Feature Vectors - Completed at %s" %time.ctime())
  print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))
  print("--- %s images processed ---------" %i)
    
# get_image_feature_vectors(['https://iw-spring.s3.amazonaws.com/uploads/figgy_prod_86_0f_8a_860f8ae166d24203b4550943656f80b0_intermediate_file.jp2.jpg', 'https://iw-spring.s3.amazonaws.com/uploads/figgy_prod_87_7e_71_877e71e97d0243ee8fa4fc9d02bddb40_intermediate_file.jp2.jpg', 'https://iw-spring.s3.amazonaws.com/uploads/figgy_prod_96_83_0f_96830fc3be264b43956bf5c66464d87d_intermediate_file.jp2.jpg', 'https://iw-spring.s3.amazonaws.com/uploads/test.cropped.jpg', 'https://iw-spring.s3.amazonaws.com/uploads/test.jpg', 'https://iw-spring.s3.amazonaws.com/uploads/figgy_prod_66_cd_fe_66cdfe155abc4132800ec2fb73a69d8b_intermediate_file.jp2.jpg'])
