from flask import Flask, render_template, url_for
import os
app = Flask(__name__)

curr_build_info = open(
    './pipeline/curr_build_info.txt', "r").read().split("\n")
print(curr_build_info)
curr_build_info = curr_build_info[1:]
curr_build_info[0] = curr_build_info[0][1:]
curr_build_info[1] = curr_build_info[1].split("=")[1]
curr_build_info[2] = curr_build_info[2].split("=")[1]
curr_build_info[3] = curr_build_info[3].split("=")[1]
curr_build_info = curr_build_info[:-1]


def parse_file(filename):
    f = open('./pipeline/info/'+filename, 'r')
    attributes = filename.split('_')
    attributes[1] = attributes[1].replace(".txt", "")
    content = f.read().split("\n")
    content = content[1:]
    content[0] = content[0][1:]
    content[1] = content[1].split("=")[1]
    content[2] = content[2].split("=")[1]
    content[3] = content[3].split("=")[1]
    content = content[:-1]
    # comparing with current build version
    flag = True
    for i in range(len(curr_build_info)):
        if(curr_build_info[i] != content[i]):
            flag = False
    content.append(0) if flag == False else content.append(1)
    attributes += content
    return attributes


@app.route('/')
def dashboard():
    successful = 0
    info = dict()
    filenames = [f for f in os.listdir(
        './pipeline/info') if os.path.isfile(os.path.join('./pipeline/info', f))]
    for name in filenames:
        info[name[:name.find('_')]] = parse_file(name)
        if(info[name[:name.find('_')]][-1] == 1):
            successful += 1
    latest = info[filenames[0][:filenames[0].find('_')]][2]
    return render_template("index.html", version_info=info, percent=str((1/len(info))*100)+"%", latest_build=latest, successful=successful)


if __name__ == '__main__':
    app.run(debug=True)
