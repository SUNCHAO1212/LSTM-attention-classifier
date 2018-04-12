
from pymongo import MongoClient
import time
import os




def mongo_download():
    HOST = ['121.40.150.141', '192.168.1.251']
    PORT = 27017
    client = MongoClient(host=HOST[0], port=PORT)
    client.admin.authenticate("liangzhi", "liangzhi123$")
    db = client.Labeling_system
    coll = db.cropus
    for docu in coll.find({'taskID': 17}):  # taskID: 13, 92, 95
        label = docu['cropus']['themes'][0]['theme']
        sent = docu['cropus']['raw']
        print(label, sent)
        # with open(label, 'a') as fo:
        #     fo.write(clean_cut_sent(sent) + '\n')
        with open(label + '_raw', 'a') as fo:
            fo.write(sent + '\n')


def make_dataset(filelist, outputfile):
    with open(outputfile, 'w') as fo:
        for filename in filelist:
            with open(filename) as f:
                for line in f:
                    fo.write(clean_cut_sent(line) + '\n')
    print("Make dataset:%s" % outputfile)

def clean_repeat(filelist):
    for filename in filelist:
        with open(filename + '_cleaned', 'w') as fo:
            with open(filename) as f:
                sent_list = [line for line in f]
                sent_set = set(sent_list)
                print(len(sent_list))
                print(len(sent_set))
                for sent in sent_set:
                    fo.write(sent)


if __name__ == '__main__':
    # mongo_download()

    # os.chdir('/home/sunchao/code/git/upload/LSTM-attn-softmax_classifier')
    # from business_processing import clean_cut_sent
    # make_dataset(['datasets/v1_需要_raw','datasets/v2_需要_raw','datasets/v3_需要_raw'], 'datasets/需要_123')
    # make_dataset(['datasets/v1_不需要_raw','datasets/v2_不需要_raw','datasets/v3_不需要_raw'], 'datasets/不需要_123')

    clean_repeat(['不需要_123', '需要_123'])