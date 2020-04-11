"""
Detects Cars in an image using KittiSeg.

Input: Image
Output: Image (with Cars plotted in Green)

Utilizes: Trained KittiSeg weights. If no logdir is given,
pretrained weights will be downloaded and used.

Usage:
python demo.py --input_image data/demo.png [--output_image output_image]
                [--logdir /path/to/weights] [--gpus 0]

--------------------------------------------------------------------------------

The MIT License (MIT)

Copyright (c) 2017 Marvin Teichmann

Details: https://github.com/MarvinTeichmann/KittiSeg/blob/master/LICENSE
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import os
import sys

import collections

# configure logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

# https://github.com/tensorflow/tensorflow/issues/2034#issuecomment-220820070
import numpy as np
import scipy as scp
import scipy.misc
import tensorflow as tf
import cv2
import matplotlib
flags = tf.app.flags
FLAGS = flags.FLAGS


#inputdir = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_heading-1_noPolylines\\"
inputdir = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_varHeading_fov90\\teste2\\"
#inputdir = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_varHeading_fov90\\train + val\\"
dirResName = '\\results\\'


sys.path.insert(1, 'incl')

from seg_utils import seg_utils as seg

try:
    # Check whether setup was done correctly

    import tensorvision.utils as tv_utils
    import tensorvision.core as core
except ImportError:
    # You forgot to initialize submodules
    logging.error("Could not import the submodules.")
    logging.error("Please execute:"
                  "'git submodule update --init --recursive'")
    exit(1)


flags.DEFINE_string('logdir', None,
                    'Path to logdir.')
flags.DEFINE_string('input_image', None,
                    'Image to apply KittiSeg.')
flags.DEFINE_string('output_image', None,
                    'Image to apply KittiSeg.')


default_run = 'KittiSeg_pretrained'
weights_url = ("ftp://mi.eng.cam.ac.uk/"
               "pub/mttt2/models/KittiSeg_pretrained.zip")


def maybe_download_and_extract(runs_dir):
    logdir = os.path.join(runs_dir, default_run)

    if os.path.exists(logdir):
        # weights are downloaded. Nothing to do
        return

    import zipfile
    download_name = tv_utils.download(weights_url, runs_dir)

    logging.info("Extracting KittiSeg_pretrained.zip")

    zipfile.ZipFile(download_name, 'r').extractall(runs_dir)

    return


def resize_label_image(image, gt_image, image_height, image_width):
    image = scp.misc.imresize(image, size=(image_height, image_width),
                              interp='cubic')
    shape = gt_image.shape
    gt_image = scp.misc.imresize(gt_image, size=(image_height, image_width),
                                 interp='nearest')

    return image, gt_image

def convertToHSV(rgb_image):
    norm_image = rgb_image;
    norm_image = cv2.normalize(rgb_image,norm_image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    image_hsv = matplotlib.colors.rgb_to_hsv(norm_image)
    image_hsv = cv2.normalize(image_hsv,image_hsv, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return image_hsv

def main(_):
    blank_image = scp.misc.imread('blank_image_google.png')
    output_dir_raw=''
    output_dir_raw=output_dir_raw+FLAGS.logdir
    output_dir_raw=output_dir_raw+dirResName
    print(output_dir_raw)
    
    os.makedirs(output_dir_raw, exist_ok=True)
    
    tv_utils.set_gpus_to_use()

    # if FLAGS.input_image is None:
    #     logging.error("No input_image was given.")
    #     logging.info(
    #         "Usage: python demo.py --input_image data/test.png "
    #         "[--output_image output_image] [--logdir /path/to/weights] "
    #         "[--gpus GPUs_to_use] ")
    #     exit(1)

    if FLAGS.logdir is None:
        # Download and use weights from the MultiNet Paper
        if 'TV_DIR_RUNS' in os.environ:
            runs_dir = os.path.join(os.environ['TV_DIR_RUNS'],
                                    'KittiSeg')
        else:
            runs_dir = 'RUNS'
        maybe_download_and_extract(runs_dir)
        logdir = os.path.join(runs_dir, default_run)
    else:
        logging.info("Using weights found in {}".format(FLAGS.logdir))
        logdir = FLAGS.logdir

    # Loading hyperparameters from logdir
    hypes = tv_utils.load_hypes_from_logdir(logdir, base_path='hypes')

    logging.info("Hypes loaded successfully.")

    # Loading tv modules (encoder.py, decoder.py, eval.py) from logdir
    modules = tv_utils.load_modules_from_logdir(logdir)
    logging.info("Modules loaded successfully. Starting to build tf graph.")

    # Create tf graph and build module.
    with tf.Graph().as_default():
        # Create placeholder for input
        image_pl = tf.placeholder(tf.float32)
        image = tf.expand_dims(image_pl, 0)

        # build Tensorflow graph using the model from logdir
        prediction = core.build_inference_graph(hypes, modules,
                                                image=image)

        logging.info("Graph build successfully.")

        # Create a session for running Ops on the Graph.
        sess = tf.Session()
        saver = tf.train.Saver()

        # Load weights from logdir
        core.load_weights(logdir, sess, saver)

        logging.info("Weights loaded successfully.")

    
    
    
    for streetname in os.listdir(inputdir):   
        ##trocar linha comentada abaixo pelas posteriores
        streetpath = os.path.join(inputdir,streetname)
        #streetpath = inputdir
        #streetname = 'unica'
        output_dir_raw_currentstreet = os.path.join(output_dir_raw,streetname)
        
        print("output_dir_raw_currentstreet: "+output_dir_raw_currentstreet)
        #input('parada:')
        os.makedirs(output_dir_raw_currentstreet, exist_ok=True)
        
        

        for filename in os.listdir(streetpath):
            
            input_image = os.path.join(streetpath,filename)
            
            logging.info("Starting inference using {} as input".format(input_image))

            # Load and resize input image
            image = scp.misc.imread(input_image)

            width, height, z = blank_image.shape
            isBlank = True;
            for i in range(width):
                for j in range(height):
                    if blank_image[i,j,0] != image[i,j,0] or blank_image[i,j,1] != image[i,j,1] or blank_image[i,j,2] != image[i,j,2]:
                        isBlank = False
                        break
                if isBlank == False:
                    break
            
            if isBlank:
                continue

            
            
            
            if hypes['jitter']['reseize_image']:
                # Resize input only, if specified in hypes
                image_height = hypes['jitter']['image_height']
                image_width = hypes['jitter']['image_width']
                image = scp.misc.imresize(image, size=(image_height, image_width),
                                          interp='cubic')
            #image = convertToHSV(image)
            # classes
            classes_colors =  [ hypes['data']['background_color'], hypes['data']['paved_road_color'], hypes['data']['nonpaved_road_color'] , hypes['data']['rocks_road_color']]
            #classes_colors =  [ hypes['data']['background_color'], hypes['data']['paved_road_color'], hypes['data']['nonpaved_road_color'] ]

            # Run KittiSeg model on image
            feed = {image_pl: image}
            softmax = prediction['softmax']
            output = sess.run(softmax, feed_dict=feed)

            # Reshape output from flat vector to 2D Image
            shape = image.shape
            output_image = output.reshape(shape[0], shape[1], -1)

            x = np.argmax(output_image,axis=2)
            im = np.zeros((shape[0], shape[1],3), dtype=np.uint8)
            for i,_ in enumerate(x):
                for j,_ in enumerate(x[i]):
                    value = x[i][j]
                    color_code  = classes_colors[value]
                    im[i][j] = color_code


            # Save output images to disk.
            if FLAGS.output_image is None:
                output_base_name = input_image
            else:
                output_base_name = FLAGS.output_image

            raw_image_name = filename.split('.png')[0] + '_raw.png'
            #print('============= '+output_dir_raw_currentstreet)
            #print('============= '+raw_image_name)
            #print('============= '+os.path.join(output_dir_raw_currentstreet, raw_image_name))
            #input('parada:')
            scp.misc.imsave(os.path.join(output_dir_raw_currentstreet, raw_image_name), im)

if __name__ == '__main__':
    tf.app.run()
