from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance
import requests
import os
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1 MB limit for uploaded files
UPLOAD_FOLDER = './uploads'  # папка для загруженных файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
RECAPTCHA_SITE_KEY = '6Lfs0AImAAAAABSmeuEXTXv-AMvFwww6VOT2biDx'


# Image resizing endpoint
@app.route('/adjust_brightness', methods=['POST'])
def adjust_brightness():
    # read the uploaded image file
    img_file = request.files['image']
    img = Image.open(img_file)

    # get the brightness level from the POST request
    brightness = int(request.form['brightness'])

    # adjust the brightness of the image using Pillow and NumPy
    img_array = np.array(img)
    img_array = np.clip(img_array + brightness, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)

    # create histograms of the color distributions of both the original and adjusted images
    generate_histogram(img)
    generate_histogram(Image.fromarray(np.array(Image.open(img_file))))

    return "Image processed successfully!"


def generate_histogram(image):
    # convert image to grayscale and then to NumPy array
    img_array = np.array(image.convert('L'))

    # compute histogram
    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])

    # plot histogram
    plt.hist(img_array.flatten(), 256, [0, 256], color='r')
    plt.xlim([0, 256])
    plt.ylim([0, 10000])
    plt.xlabel('Pixel value')
    plt.ylabel('Frequency')
    plt.show()


if __name__ == '__main__':
    app.run(debug=True)