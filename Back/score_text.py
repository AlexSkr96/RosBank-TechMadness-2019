import os
import json
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

@app.route("/score_text/<string:txt>/<string:type>")
def score_text(txt, type='text'):

  # Possible types:
  # 'Subject' for subject of the ticket
  # 'Text' for body text of the ticket
  # 'File' for attached files
  # PROPOSAL: can front keep track of the order in wich files were uploaded?
  #   If so, send 'file0', 'file1' and so on
  
  f_scores = open('/mnt/c/Resources/TechMadness/db/scores.json', 'r')
  scores_dict = json.load(f_scores)

  for key_word, costs in scores_dict.items():
    amount = txt.lower().count(key_word.lower())
    for topic,topic_value in costs.items():
      if (topic_value*amount) != 0:
        globscores[topic]['value'] += (topic_value*amount)/len(txt.split(' '))

  return json.dumps(list(globscores.values()))
  # os.popen('tesseract /mnt/c/Resources/TechMadness/task.jpg stdout -l eng+rus').read()