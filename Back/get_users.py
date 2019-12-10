from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='/mnt/c/Resources/TechMadness/')
app.secret_key = "secret key"
UPLOAD_FOLDER = '/mnt/c/resources/TechMadness/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

@app.route("/get_users")
def get_users():
    f = open('/mnt/c/Resources/TechMadness/db/users.json', 'r')
    txt = f.read()
    return txt