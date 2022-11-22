import os
import test1
import mysql.connector
import bcrypt
import cv2
from flask import Flask, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "fileUpload"


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/register', methods=["POST"])
def register():
    # Getting the arguments from the URL
    name = request.form.get('name')
    username = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('pass')

    # Hashing the password
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(byte, salt)

    # Checking if user already exists
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='chequesystem')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR mail = '{mail}'")
    res = cursor.fetchall()
    if len(res) != 0:
        return 'user exists'

    # Inserting user data
    query = 'INSERT INTO users (name, username, mail, password) VALUES(%s, %s, %s, %s)'
    val = (name, username, mail, password)
    cursor.execute(query, val)
    conn.commit()
    return 'Successful'


@app.route('/login', methods=["POST"])
def login():
    # Getting the arguments from the URL
    mail = request.form.get('mail')
    password = request.form.get('pass')

    # Hashing the password
    password = password.encode('utf-8')

    # Checking if user already exists
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='chequesystem')
    cursor = conn.cursor()

    cursor.execute(f"SELECT password FROM users WHERE mail = '{mail}'")
    res = cursor.fetchall()
    if len(res) == 0:
        return 'Invalid Username'
    if bcrypt.checkpw(password, res[0][0].encode('utf-8')):
        return 'Successful'
    return 'Invalid Password'


@app.route('/upload', methods=["POST"])
def upload():
    f = request.files['selectedFile']
    validExt = ['png', 'jpg', 'jpeg', 'tif', 'eps', 'gif']
    extension = f.filename.split('.')[1]
    if extension not in validExt:
        return "Not a valid extension"

    fname = secure_filename(str(len(os.listdir('fileUpload')))) + "." + extension
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
    img = cv2.imread("fileUpload\\" + fname)
    res = test1.crop(img, fname)
    res["imgUrl"] = fname
    res["date"] = res["date"][:2] + "/" + res["date"][2:4] + "/" + res["date"][4:]
    return res


@app.route('/get_image', methods=["POST"])
def get_image():
    fname = request.form.get("name")
    imgPath = os.path.abspath("fileUpload/procFile/" + fname)
    return imgPath


@app.route('/saveDetails', methods=["POST"])
def saveDetails():
    # Get Parameters from the request
    username = request.form.get('username')
    name = request.form.get('name')
    amt = request.form.get('amt')
    date = request.form.get('date')
    accNo = request.form.get('accNo')
    amtWord = request.form.get('amtWord')
    fname = request.form.get('file')

    # Creating a database cursor
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='chequesystem')
    cursor = conn.cursor()

    # Inserting user data
    query = 'INSERT INTO cheque(username, payName, amt, accNo, date, amtWord, fname) VALUES(%s, %s, %s, %s, %s, %s, %s)'
    val = (username, name, amt, accNo, date, amtWord, fname)
    cursor.execute(query, val)
    conn.commit()
    return "Successful"


@app.route('/getDetails', methods=["GET"])
def getDetails():
    username = request.args.get("username")
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='chequesystem')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM cheque WHERE username = '{username}'")
    data = cursor.fetchall()
    res = []
    for i, d in enumerate(data):
        temp = {'sNo': i, 'name': d[2], 'amt': d[3], 'accNo': d[4], 'date': d[5], 'amtWord': d[6]}
        res.append(temp)
    return res


if __name__ == '__main__':
    app.run()
