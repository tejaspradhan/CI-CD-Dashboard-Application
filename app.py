import helper
from flask import Flask, render_template, url_for
import os
app = Flask(__name__)


@app.route('/')
def dashboard():
    successful = 0
    info = dict()
    filenames = [f for f in os.listdir(
        './pipeline/info') if os.path.isfile(os.path.join('./pipeline/info', f))]
    for name in filenames:
        info[name[:name.find('_')]] = helper.parse_file(name)
        if(info[name[:name.find('_')]][-1] == 1):
            successful += 1
    latest = info[filenames[0][:filenames[0].find('_')]][2]
    return render_template("index.html", version_info=info, percent=str((1/len(info))*100)+"%", latest_build=latest, successful=successful)


if __name__ == '__main__':
    app.run(debug=True)
