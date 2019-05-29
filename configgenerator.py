import json

jsondata = {
    "cuda" : "true",
    "choidataset": "/home/ec2-user/ELS/py3/clean_/data/data-micoros-nz-clean/",
}

with open('config.json', 'w') as f:
    json.dump(jsondata, f)
