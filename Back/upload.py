from flask import Flask
import os
#import magic
import urllib.request
# from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
# import docx
import pandas

# CORS(app)

ALLOWED_EXTENSIONS = set(['txt','csv','json','docx','xlsx','png','jpg','jpeg'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def upload_form():
  return render_template('test_upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
  images = ['png','jpg','jpeg']
  texts  = ['txt','csv','json']
    
  if request.method == 'POST':
        # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No file selected for uploading')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      file_ext = file.filename.split('.')[-1]
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      flash('File successfully uploaded')
      
      text = ''
      if file_ext in images:
        text = os.popen(f'tesseract /mnt/c/Resources/TechMadness/{file.filename} stdout -l eng+rus').read()
        print(type(text))
      elif file_ext == 'xlsx':
        text = file.to_csv(file,index=False,header=None,encoding='utf-8').read()
#       elif file_ext == 'docx':
#         full_text = []
#         doc = docx.Document(file)
#         for para in doc.paragraphs:
#           full_text.append(para.text)
#         text = '\n'.join(full_text)
      elif file_ext in texts:
        text = file.read()
      print(score_text(text))
      return score_text(text)
#       return 'OK'
    else:
      flash('Allowed file types are txt, csv, json, docx, xlsx, png, jpg, jpeg')
      return redirect(request.url)