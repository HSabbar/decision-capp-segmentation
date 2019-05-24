import json

jsondata = {
    "cuda" : "true",
    "choidataset": "/home/ec2-user/ELS/py3/clean_/decision-capp-segmentation/data/data-n-micros/",
}

with open('config.json', 'w') as f:
    json.dump(jsondata, f)
