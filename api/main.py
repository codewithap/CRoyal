
from flask import Flask, render_template,request
import requests
import datetime
from datetime import timedelta
import maya

app = Flask(__name__)

@app.route("/")  #  home page  #
def hello():
    url = "https://proxy.royaleapi.dev/v1/clans/%23QPRGGRJQ"
    #  API key  # 
    file = open("key.txt","r")
    my_key = file.read()
    file.close()
    headers = {
        'Accept': "application/json",
        'authorization': "Bearer %s" % my_key
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)

    mArrey = data['memberList']
    now = datetime.datetime.now()
    now2 = maya.parse(now).datetime()
    i = 0
    lsArr = []
    dayArr = []
    H_arr = []
    M_arr = []

    while i < data['members']:
        lastSeen = mArrey[i]['lastSeen']
        lastSeen2 = maya.parse(lastSeen).datetime()
        lastOnline = ((now2 + timedelta(hours=24, minutes=18)) - lastSeen2)
        i += 1
        dayArr.append(lastOnline.days) 
        H_arr.append(int(((lastOnline.seconds)/60)/60))
        minutes = ((((lastOnline.seconds)/60)/60) - int(((lastOnline.seconds)/60)/60))
        M_arr.append(int(minutes * 60)) 
    # print(dayArr,"\n",H_arr,"\n",M_arr)
    return render_template('index.html', data = data,mArrey = mArrey, dayArr = dayArr,H_arr = H_arr,M_arr = M_arr)
 
    #________errorhandlers_________#

@app.route("/key", methods = ["GET","POST"])
def key():
  url = "https://proxy.royaleapi.dev/v1/clans/%23QPRGGRJQ"
      #  API key  #
  file = open("key.txt","r")
  my_key = file.read()
  file.close()
  headers = {
    'Accept': "application/json",
    'authorization': "Bearer %s" % my_key
  }
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  print(data)
  if request.method == "POST": 
    key = request.form["key"]
    f = open("key.txt","w")
    f.write(key)
    f.close()
  return render_template("key.html",data = data)

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')
if __name__=="__main__":
    app.run(host="0.0.0.0")
