import os
import json
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

@app.route("/score_text/<string:txt>/<string:theme>")
def score_text(txt, theme='true'):
#   if len(txt.split(' ')) < 4 and theme.lower() != 'true':
  
  f_scores = open('/mnt/c/Resources/TechMadness/db/scores.json', 'r')
  scores_dict = json.load(f_scores)

  for key_word, costs in scores_dict.items():
      amount = txt.lower().count(key_word.lower())
      for topic,topic_value in costs.items():
        if (topic_value*amount) != 0:
            globscores[topic]['value'] += (topic_value*amount)/len(txt.split(' '))

  return json.dumps(list(globscores.values()))
  # os.popen('tesseract /mnt/c/Resources/TechMadness/task.jpg stdout -l eng+rus').read()