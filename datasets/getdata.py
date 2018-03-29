
from pymongo import MongoClient
import time
import os

from business_processing import clean_cut_sent


def mongo_download():
    HOST = ['121.40.150.141', '192.168.1.251']
    PORT = 27017
    client = MongoClient(host=HOST[1], port=PORT)
    # client.admin.authenticate("liangzhi", "liangzhi123$")
    db = client.Labeling_system
    coll = db.cropus
    for docu in coll.find({'taskID': 92}):  # taskID: 13, 92, 95
        label = docu['cropus']['themes'][0]['theme']
        sent = docu['cropus']['raw']
        print(label, sent)
        with open(label, 'a') as fo:
            fo.write(clean_cut_sent(sent) + '\n')
        with open(label + '_raw', 'a') as fo:
            fo.write(sent + '\n')


if __name__ == '__main__':
    start_time = time.time()

    mongo_download()

    end_time = time.time()
    print(end_time-start_time)