import os
from flask import Flask, render_template, request, redirect, url_for, session, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'

def submit():
    if not session.get('user'):
        session['result'] = None
        session['user'] = str(datetime.now()).replace(':', '')
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        folder_path = os.path.join(app.config['UPLOAD_PATH'], session.get('user'))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        result_path = os.path.join(folder_path, 'result', 'text.txt')
        if os.path.exists(result_path):
            os.remove(result_path)
        uploaded_file.save(os.path.join(folder_path, filename))
        session['filename'] = filename
        while not os.path.isfile(result_path):
            time.sleep(1)
        f = open(result_path, 'r')
        session['result'] = f.read()
        f.close()

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/', methods=['GET'])
def index():
    if not session.get('user'):
        session['result'] = None
        session['user'] = str(datetime.now()).replace(":", "")
    # files = os.listdir(app.config['UPLOAD_PATH'])
    # return render_template('index.html', files=files)
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():
    submit()
    return redirect(url_for('index'))

@app.route('/app', methods=['POST'])
def application():
    submit()
    return str(round(float(session.get('result').split('dogs ')[1].split('%')[0]) / 100, 4)), 200

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_PATH'], session.get('user')), filename)

if __name__ == '__main__':
    app.run(debug = True)
