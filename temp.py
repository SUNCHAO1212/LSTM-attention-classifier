
from pymongo import MongoClient
import hashlib
import time
import re

from interface import interface

filtrate = re.compile(u'[^\u4E00-\u9FA5a-zA-Z0-9]')

def clean_content(sentence):
    """ Clean """
    sentence = re.sub('<.+?>', '', sentence)
    sentence = re.sub('\\\\t', '', sentence)
    sentence = re.sub('\\\\n', '', sentence)
    sentence = re.sub('\t', '', sentence)
    sentence = re.sub('\n', '', sentence)
    # sentence = filtrate.sub(r' ', sentence)

    return sentence


def md5sum(cont):

    fmd5 = hashlib.md5(cont)
    # print(fmd5)
    return fmd5


def upload(docu, cnt=-1):
    client = MongoClient(host='121.40.150.141', port=27017)
    client.admin.authenticate("liangzhi", "liangzhi123$")
    db_temp = client.Labeling_system
    coll = db_temp.emotional_analysis_testset

    title = docu['title']
    url = docu['url']
    # create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    publish_time = docu['events'][0]['eventTime']['formatTime']
    # rawId = str(docu['_id'])
    content = clean_content(docu['content'])
    md5 = str(md5sum(content.encode('utf8')))
    theme = '中性' if interface(title) == '无' else '消极'

    # print(cnt,title,url,create_time,rawId,md5.hexdigest(),theme)

    temp_dict={
        "nafVer": {
        "lang": "cn",
        "version": "v1.0",
        "projectInfo": {
            "desc": "情感分析_孙超",
            "projectType": "文本分类",
            "projectID": "12"
        }
        },
        "raw": title,
        "nafHeader": {
            "content": content,
            "title": title,
            "url": url,
            "publishTime": publish_time,
            "id": cnt,
            "docId": md5
        },
        "themes": [
        {
            "theme": theme,
            "id": "theme0",
            "externalReferences": [
            {
                "resource": "resouces名称",
                "reference": "uri地址"
            }
          ]
        }
      ]
    }

    print(temp_dict["nafHeader"]['id'], temp_dict['themes'][0]['theme'],temp_dict["nafHeader"]['publishTime'])

    coll.save(temp_dict)


def main1():

    conn = MongoClient(host='192.168.1.251', port=27017)
    # conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.TianJi
    # db = conn.test
    cnt = 0
    for document in db.hzgz_tianyu1.find({"events.eventTime.formatTime": {"$gt":'2018-01-01 00:00:00'}}):
        try:
            if document['language'] == 'zh':
                cnt += 1
                upload(document, cnt)
                # print(cnt, document['title'], document['events'][0]['eventTime']['formatTime'])
                if cnt > 5000:
                    break
            else:
                pass
        except KeyError:
            print(KeyError)


def change_docu():
    conn = MongoClient(host='121.40.150.141', port=27017)
    conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.Labeling_system
    coll = db.emotional_analysis_testset
    i = 0
    for docu in coll.find({}):

        i += 1
        label = '中性'
        title = docu['nafHeader']['title']
        risk_level = interface(title)
        if risk_level == '无':
            label = '中性'
        elif risk_level in ['高', '中', '低']:
            label = '消极'
        else:
            print('Error.')
        print(i, label, docu['_id'])
        coll.update({"_id": docu['_id']}, {'$set': {"themes.0.theme":label}})


if __name__ == "__main__":

    # main1()
    change_docu()

