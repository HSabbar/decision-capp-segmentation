import json

jsondata = {
    "cuda" : "true",
    "choidataset": "/home/ec2-user/ELS/py3/clean_/data/2xArchi-data/",
}

with open('config.json', 'w') as f:
    json.dump(jsondata, f)
