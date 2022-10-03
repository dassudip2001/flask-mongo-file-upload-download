from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mongoengine import  MongoEngine  # ModuleNotFoundError: No module named 'flask_mongoengine' = (venv) C:\flaskmyproject>pip install flask-mongoengine
from werkzeug.utils import secure_filename
# from pymongo import MongoClient
import os
import datetime
import pymongo
# import magic
import urllib.request

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
    meta=db.index("timestamp", expireAfterSeconds=3*60)
   
  
    

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    inputEmail = request.form['inputEmail']
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


if __name__ == '__main__':
    app.run(debug=True)