import datetime
import time
import time
from playsound import playsound
from datetime import datetime
import os
import requests

def classify(path):
    response = requests.post('http://127.0.0.1:5000/app', files=dict(file=open(path, 'rb')))
    acc = float(response.text)
    return acc

cap_dir = 'captures'
rec_dir = 'images'
rec_path = 'records/record.txt'
alert_path = 'alert.mp3'

while True:
    for filename in os.listdir(cap_dir):
        print('File is found')
        f = os.path.join(cap_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            acc = classify(f)
            if acc >= 0.7:
                os.rename(f, os.path.join(rec_dir, filename))
                playsound(alert_path, False)
                r = open(rec_path, 'a')
                r.write(str(datetime.now()) + ' ' + filename + ' ' + str(acc) + '\n')
                r.close()
            else:
                os.remove(f)
    print('Go to the next loop')
    time.sleep(1)
