

from pymongo import MongoClient
from main import train_predict

from business_processing import *


def interface(sent, flag='zh'):
    """
    :param sent: the sentence to predict
    :param flag: language flag, 'zh'(Chinese) or 'en'(English)
    :return: risk_level:'高', '中', '低', '无'
    """
    sent = clean_cut_sent(sent)
    risk_level = '无'
    if flag == 'zh':
        # if input_filter(sent):
        #     pass
        # else:
        #     return '无'
        label = train_predict(sent)  # negative, neutral
        risk_level = chinese_risk_level(sent, label)
    elif flag == 'en':
        risk_level = english_risk_level(sent)
    else:
        print("Please check language flag")
    return risk_level


if __name__ == '__main__':

    HOST = '192.168.1.251'
    PORT = 27017

    conn = MongoClient(host=HOST, port=PORT)
    db = conn.TianJi
    cnt = 1
    with open('record/record_sent.txt', 'a') as fo:
        for i in db.hzgz_tianyu1.find({'events.eventTime.mention':{'$gte':'2017-12-09 00:00:00'},'crawOpt.siteType':{"$regex":"官方网站"}}):
            attn_value = []
            pre_value = []
            result = interface(i['title'])
            print(cnt, clean_cut_sent(i['title']), result)
            fo.write(clean_cut_sent(i['title']) + '\n')
            cnt += 1


