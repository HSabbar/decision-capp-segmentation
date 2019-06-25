import json

jsondata = {
    "cuda" : "true",
    "choidataset": "/home/ec2-user/ELS/Zoning-micro/data/decisions-data/without-Title/",
}

with open('config.json', 'w') as f:
    json.dump(jsondata, f)
