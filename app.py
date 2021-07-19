import helper
from flask import *
import urllib
import os
import json
from json2html import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "Yash"

PIPELINES = []
ALL_VM_STATUS = []

def pipelines():
    global PIPELINES
    PIPELINES = [f for f in os.listdir('../') if(f.find("tmp")==-1 and f.find("@libs")==-1)]
    # print(PIPELINES)
    PIPELINES.remove("CI-CD-Dashboard-Application")
    # print(PIPELINES)
    for x in PIPELINES:
        if(os.path.isdir('../'+x+'/info')):
            dir = os.listdir('../'+x+'/info')
            if(len(dir)==0):
                PIPELINES.remove(x)
        else:
            PIPELINES.remove(x)

def all_vm_status():
    global ALL_VM_STATUS
    f = open('../Health_Check/logfile.txt', 'r')
    content = f.read().split("\n")
    for x in content:
        if(len(x)<2):
            continue
        ALL_VM_STATUS.append(x.split(" : "))


@app.errorhandler(404)
def not_found(e):
  return render_template("error.html", status=404)

@app.route('/')
def dashboard():
    try:
        return render_template("index.html", text="Please Select Project To Display Status", pipelines=PIPELINES, all_status=ALL_VM_STATUS)
    except:
        return render_template("error.html", status=500)

@app.route('/report', methods=['POST', 'GET'])
def fetch():
    try:
        appname = ""
        if request.method=="GET":
            appname = session['appname']
        else:
            appname = request.form['app']
        successful = 0
        info = dict()
        filenames = [f for f in os.listdir(
            '../'+ appname +'/info') if os.path.isfile(os.path.join('../'+ appname +'/info', f))]
        for name in filenames:
            info[name[:name.find('-')]] = helper.parse_file(name, appname)
            if(info[name[:name.find('-')]][-2] == 1):
                successful += 1
        latest = info[filenames[0][:filenames[0].find('-')]][2]
        session['appname'] = appname
        
        dbinfo = []
        dbinfo = helper.get_dbinfo(appname)

        return render_template("index.html", version_info=info, percent=str((successful/len(info))*100)+"%", latest_build=latest, successful=successful, pipelines=PIPELINES, appname=appname, dbinfo=dbinfo)
    except Exception as e:
        print(e)
        return render_template("error.html", status=500)

@app.route('/health',methods=['GET','POST'])
def healthcheck():
    try:
        PORT = helper.get_port(session['appname'])
        ip = request.form['ip']
        response = urllib.request.urlopen("http://"+ip+":"+PORT+"/actuator/health")
        data = response.read()
        data = json.loads(data)
        code = json2html.convert(json = data, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        # print(code)
        return render_template("health.html", data=data, code=code, ip=ip)
    except Exception as e:
        print(e)
        return render_template("error.html", status=500)

@app.route('/error')
def error():
    return render_template("error.html")

if __name__ == '__main__':
    pipelines()
    all_vm_status()
    app.run(debug=True)
