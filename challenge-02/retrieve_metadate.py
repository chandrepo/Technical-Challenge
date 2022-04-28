import requests
import json

metadataUrl = 'http://169.254.169.254/latest/'


def traverse_tree(url, arr):
    output = {}
    for item in arr:
        newUrl = url + item
        r = requests.get(newUrl)
        text = r.text
        if item[-1] == "/":
            listValues = r.text.splitlines()
            output[item[:-1]] = traverse_tree(newUrl, listValues)
        elif isJson(text):
            output[item] = json.loads(text)
        else:
            output[item] = text
    return output


def get_metadata():
    initial = ["meta-data/"]
    result = traverse_tree(metadataUrl, initial)
    return result


def get_metadata_json():
    metadata = get_metadata()
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json


def isJson(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    print(get_metadata_json())
