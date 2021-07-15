import xml.etree.ElementTree as ET
import urllib
import json
from json2html import *

def get_latest_version(appname):
    tree = ET.parse("../"+ appname +"/pom.xml")
    root = tree.getroot()
    namesp = root.tag.replace("project", "")
    parent = root.find(namesp+"parent")
    return parent.find(namesp+"version").text

def get_port(appname):
    f = open("../"+appname+"/src/main/resources/application.properties", 'r')
    l = f.read().split("\n")
    d = dict()
    for i in l:
        if(i.find("=")==-1):
            continue
        key, val = i.split("=")
        d[key] = val
    return d['server.port']


def parse_file(filename, appname):
    CURR_VERSION = get_latest_version(appname)
    PORT = get_port(appname)
    f = open('../'+ appname +'/info/'+filename, 'r')
    attributes = filename.split('-')
    attributes[1] = attributes[1].replace(".txt", "")
    content = f.read().split("\n")
    content = content[1:]
    content[0] = content[0][1:]
    content[1] = content[1].split("=")[1]
    content[2] = content[2].split("=")[1]
    content[3] = content[3].split("=")[1]
    content = content[:-1]
    # comparing with current build version
    content.append(1) if CURR_VERSION == content[1] else content.append(0)
    # print(appname, CURR_VERSION, content[1])
    attributes += content
    try:
        response = urllib.request.urlopen("http://"+attributes[1]+":"+PORT+"/actuator/health")
        data = response.read()
        data = json.loads(data)
        attributes.append(data['status'])
    except Exception as e:
        attributes.append("DOWN")
    # print(attributes)
    return attributes
