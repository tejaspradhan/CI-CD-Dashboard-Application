import xml.etree.ElementTree as ET


def get_latest_version():
    tree = ET.parse("./pipeline/pom.xml")
    root = tree.getroot()
    namesp = root.tag.replace("project", "")
    parent = root.find(namesp+"parent")
    return parent.find(namesp+"version").text


CURR_VERSION = get_latest_version()


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
    content.append(
        0) if CURR_VERSION == content[2] else content.append(1)
    attributes += content
    return attributes
