import json

jsondata = {
    "choidataset": "/home/ec2-user/ELS/py3/clean_/text-segmentation/data/choi/1/3-11/",
}

with open('config.json', 'w') as f:
    json.dump(jsondata, f)
