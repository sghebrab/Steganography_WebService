from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, current_app
import steganography as stg
from werkzeug.utils import secure_filename
import os
import glob
import cv2

app = Flask(__name__)
# Here I'll put the pictures that users upload
app.config['UPLOAD_FOLDER'] = os.path.join("static", "uploaded_images")
# After writing a message into a picture, the picture will be saved in this folder
app.config['ELABORATED_FOLDER'] = os.path.join("static", "elaborated_images")


@app.route('/')
def homepage():
    # Each time the homepage is loaded, each picture on the server is deleted
    uploaded_images = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*"))
    for um in uploaded_images:
        os.remove(um)
    elaborated_images = glob.glob(os.path.join(app.config['ELABORATED_FOLDER'], "*"))
    for em in elaborated_images:
        os.remove(em)
    return render_template('index.html')


@app.route("/info", methods=['GET'])
def info():
    return render_template("info.html")


@app.route("/hide", methods=['POST'])
def hide():
    image = request.files['img-hide']
    # This will be the name of the elaborated picture
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    # Save on the server the picture that the user uploaded
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Then open it
    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # If it's none, then something went wrong with the file.
    if image is None:
        return render_template('write_error.html', error_msg='The picture you provided cannot be opened.')
    # Convert it to RBG since darned OpenCV uses BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Load the message
    message = request.form['msg-hide']
    # Compute the maximum length of the message using "normal" characters (max 2 bytes per character)
    message_max_length = (image.shape[0]*image.shape[1]) // 16
    # Write the message into the picture
    image = stg.write_message_to_image(image, message)
    # If image is none here but not before, then there was a problem while writing the message
    if image is None:
        error_msg = 'The message you wrote is too long for this picture. For this picture, the message should contain' \
                    ' at most ' + str(message_max_length) + " characters."
        return render_template('write_error.html', error_msg=error_msg)
    # Finally, write the elaborated image into the correct folder so that the user can download it
    cv2.imwrite(os.path.join(app.config['ELABORATED_FOLDER'], filename), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    url_download = os.path.join(app.config['ELABORATED_FOLDER'], filename)
    return render_template('hide.html', image_name=filename, message=message, image_path=url_download)


@app.route("/reveal", methods=["POST"])
def reveal():
    image = request.files['img-reveal']
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    message_revealed = stg.read_message_from_image(image)
    return render_template("reveal.html", image_path=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                           message=message_revealed)

