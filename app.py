from flask import Flask, render_template, url_for
import os
app = Flask(__name__)


def parse_file(filename):
    f = open('./pipeline/info/'+filename, 'r')
    attributes = filename.split('_')
    attributes[1] = attributes[1].replace(".txt", "")
    content = f.read().split("\n")
    content = content[1:]
    content[0] = content[0][1:]
    content = content[:-1]
    attributes += content
    return attributes


@app.route('/')
def dashboard():
    info = dict()
    filenames = [f for f in os.listdir(
        './pipeline/info') if os.path.isfile(os.path.join('./pipeline/info', f))]
    for name in filenames:
        info[name[:name.find('_')]] = parse_file(name)
    return render_template("index.html", version_info=info)


if __name__ == '__main__':
    app.run(debug=True)
