import helper
from flask import Flask, request, render_template, url_for
import os
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

PIPELINES = []

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
        

@app.route('/')
def dashboard():

    return render_template("index.html", text="Please Select Project To Display Status", pipelines=PIPELINES)

@app.route('/report', methods=['POST'])
def fetch():
    appname = request.form['app']
    successful = 0
    info = dict()
    filenames = [f for f in os.listdir(
        '../'+ appname +'/info') if os.path.isfile(os.path.join('../'+ appname +'/info', f))]
    for name in filenames:
        info[name[:name.find('-')]] = helper.parse_file(name, appname)
        if(info[name[:name.find('-')]][-1] == 1):
            successful += 1
    latest = info[filenames[0][:filenames[0].find('-')]][2]
    return render_template("index.html", version_info=info, percent=str((successful/len(info))*100)+"%", latest_build=latest, successful=successful, pipelines=PIPELINES, appname=appname)

@app.route('/temp',methods=['GET','POST'])
def healthcheck():
    #return str(requests.get("http://192.168.1.8:8090/actuator/health"))
    response = urllib.request.urlopen("http://192.168.1.8:8090/actuator/health")
    data = response.read()
    data= json.loads(data)
    print(data['status'])

    return data

if __name__ == '__main__':
    pipelines()
    app.run(debug=True)
