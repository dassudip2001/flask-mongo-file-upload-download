from io import BytesIO

from flask import Flask, render_template, flash, redirect, url_for, request,send_file
from flask_mongoengine import  MongoEngine  # ModuleNotFoundError: No module named 'flask_mongoengine' = (venv) C:\flaskmyproject>pip install flask-mongoengine
from werkzeug.utils import secure_filename
# from pymongo import MongoClient
# import os
import datetime
import pymongo
# import magic
import urllib.request

# import os, time, sys
    
# path = r"/home/sudip/Downloads/flask-docker-demo/static/img"
# now = time.time()


# for f in os.listdir(path):
#   if os.stat(f).st_mtime < now - 7 * 86400:
#     if os.path.isfile(f):
#       os.remove(os.path.join(path, f))
# import os
# import time


# def delete_old_files(root_dir_path, days):
#     files_list = os.listdir(root_dir_path)
#     current_time = time.time()
#     for file in files_list:
#         file_path = os.path.join(root_dir_path, file)
#         if os.path.isfile(file_path):
#             if (current_time - os.stat(file_path).st_birthtime) > days * 86400:
#                 os.remove(file_path)


# if __name__ == '__main__':
#     delete_old_files('/home/sudip/Downloads/flask-docker-demo/static/img', 7)


import os, time

path = "/home/sudip/Downloads/flask-docker-demo/static/img"
now = time.time()

for filename in os.listdir(path):
    filestamp = os.stat(os.path.join(path, filename)).st_mtime
    filecompare = now -1*86400
    if  filestamp < filecompare:
     print(filename)
     os.remove(os.path.join(path, filename))

# from test import mongo_db

app = Flask(__name__)
app.secret_key = "caircocoders-ednalan-2020"




# client = client = MongoClient('localhost', 27017,)

# db = client.flask_db
# todos = db.todos
app.config['MONGODB_SETTINGS'] = {
    'db': 'dbmongocrud',
    'host': 'localhost',
    'port': 27017,
    
}
# # mongo_col = MongoEngine.my_TTL_collection

# # mongo_db = mongo_con.Mongo_database
# # mongo_col = app.my_TTL_collection

# # timestamp = datetime.datetime.now()

# # db.ensure_index("date", expireAfterSeconds=3*60)
db = MongoEngine()
db.init_app(app)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    profile_pic = db.StringField()
    timestamp = datetime.datetime.now()
    
      

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload', methods=['GET','POST'])
def upload():
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    inputEmail = request.form['inputEmail']
    # date=datetime()
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        usersave = User(name=rs_username, email=inputEmail, profile_pic=file.filename)
        usersave.save()
        flash('File successfully uploaded ' + file.filename + ' to the database!')
        return redirect('/')
    else:
        flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')

@app.route('/download/upload_id') 
def download(upload_id):
    upload=Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data),attachment_filename=upload.filename,as_attachment=True)
if __name__ == '__main__':
     
    app.run(debug=True)
