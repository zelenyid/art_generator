import os
import json
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pdb

from main import main


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.secret_key = b'\xe3\xd3q\xa1\xa9l\xf2!\xc9x\x17\x97\xd31\xcd-\x9b\xc6\x0bA/)3\xf6'


def get_path_style():
    os.chdir("data/images/style")
    path = os.getcwd()
    os.chdir("../../../")
    return path


def get_path_img():
    os.chdir("data/images/content")
    path = os.getcwd()
    os.chdir("../../../")
    return path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/generate_art', methods=['GET', 'POST'])
def generate_art():
    main([(request.args['img'], request.args['style'])])
    art_filename = request.args['img'].split('.')[0] + '_' + request.args['style'].split('.')[0] + '_gen.jpg'
    art = os.path.join(os.path.join('static', 'out'), art_filename)
    return render_template('generated_art.html', art=art)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file-img' and 'file-style' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        img = request.files['file-img']
        style = request.files['file-style']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img.filename == '' or style.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if img and allowed_file(img.filename) and style and allowed_file(style.filename):
            img_filename = secure_filename(img.filename)
            style_filename = secure_filename(style.filename)
            img.save(os.path.join(app.config['IMAGE_UPLOAD_PATH'], img_filename))
            style.save(os.path.join(app.config['STYLE_UPLOAD_PATH'], style_filename))
            return redirect(url_for('generate_art', img=img_filename, style=style_filename))
    return render_template('index.html')


app.config['IMAGE_UPLOAD_PATH'] = get_path_img()
app.config['STYLE_UPLOAD_PATH'] = get_path_style()


if __name__ == '__main__':
    app.run(debug=True)
