import json
from flask import Flask
from flask_cors import CORS

@app.route("/get_user/<string:id>")
def get_user(id):
    id = int(id)
    
    f_score = open('/mnt/c/Resources/TechMadness/db/scores.json', 'r')
    jsn = f_score.read()
    score_dict = json.loads(jsn)

    global globscores
    globscores = {'subject': {}, 'message': {}, 'files': []}

    for topic in list(score_dict[list(score_dict)[0]]):
      globscores['subject'][topic] = {'name':topic, 'value':0}
      globscores['message'][topic] = {'name':topic, 'value':0}

    f_oper = open('/mnt/c/Resources/TechMadness/db/operations.json', 'r')
    jsn = f_oper.read()
    oper_list = json.loads(jsn)
    selected_opers = []
    for oper in oper_list:
      if oper['user_id'] == id:
        selected_opers.append(oper)
        for tag in oper['tags']:
          globscores[tag]['value']+=1
                
    for key, value in globscores.items():
      if value['value'] != 0:  
        globscores[key]['value'] = len(selected_opers)/value['value']

    f_user = open('/mnt/c/Resources/TechMadness/db/users.json', 'r')
    # jsn = f_user.read()
    user_list = json.load(f_user)
    for user in user_list:
      if user['id'] == id:
        the_user = user
        break

    result = {
        'user': the_user,
        'operations': selected_opers,
        'scores': globscores
    }

    jsn = json.dumps(result, ensure_ascii=False)
    return jsn