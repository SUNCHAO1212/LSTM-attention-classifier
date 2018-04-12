
from pymongo import MongoClient
import hashlib
import time
import re
import json

from interface import interface


filtrate = re.compile(u'[^\u4E00-\u9FA5a-zA-Z0-9]')


def clean_content(sentence):
    """ Clean """
    sentence = re.sub('<.+?>', '', sentence)
    sentence = re.sub('\\\\t', '', sentence)
    sentence = re.sub('\\\\n', '', sentence)
    sentence = re.sub('\\\\r', '', sentence)
    sentence = re.sub('\r', '', sentence)
    sentence = re.sub('\t', '', sentence)
    sentence = re.sub('\n', '', sentence)
    sentence = re.sub('\\\\', '', sentence)
    sentence = sentence.strip()

    return sentence


def md5sum(cont):

    fmd5 = hashlib.md5(cont)
    # print(fmd5)
    return fmd5


def upload(docu, cnt=-1):
    client = MongoClient(host='121.40.150.141', port=27017)
    client.admin.authenticate("liangzhi", "liangzhi123$")
    db_temp = client.Labeling_system
    coll = db_temp.emotional_analysis_zh

    # 选择更改字段
    # title = docu['title']
    # url = docu['url']
    # # create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    # publish_time = docu['events'][0]['eventTime']['formatTime']
    # # rawId = str(docu['_id'])
    # content = clean_content(docu['content'])
    # md5 = str(md5sum(content.encode('utf8')))
    # theme = '不需要' if interface(title) == '无' else '需要'

    # print(cnt,title,url,create_time,rawId,md5.hexdigest(),theme)

    # temp_dict={
    #     "nafVer": {
    #     "lang": "cn",
    #     "version": "v1.0",
    #     "projectInfo": {
    #         "desc": "杭州国检风险语料_孙超",
    #         "projectType": "文本分类",
    #         "projectID": "14"
    #     }
    #     },
    #     "raw": title,
    #     "nafHeader": {
    #         "content": content,
    #         "title": title,
    #         "url": url,
    #         "publishTime": publish_time,
    #         "id": cnt,
    #         "docId": md5
    #     },
    #     "themes": [
    #     {
    #         "theme": theme,
    #         "id": "theme0",
    #         "externalReferences": [
    #         {
    #             "resource": "resouces名称",
    #             "reference": "uri地址"
    #         }
    #       ]
    #     }
    #   ]
    # }

    temp_dict = docu
    temp_dict['nafHeader']['id'] = cnt
    print(temp_dict["nafHeader"]['id'], temp_dict['themes'][0]['theme'])

    # coll.save(temp_dict)


def main1():
    conn = MongoClient(host='121.40.150.141', port=27017)
    conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.Labeling_system
    coll = db.emotional_analysis_testset

    COLL = db.cropus
    ID_set = []
    for docu in COLL.find({'taskID':13}):
        id = docu['id']
        ID_set.append(id)
    # ID_set = set(ID_set)
    print(ID_set)

    cnt = 0
    for document in coll.find():

        if document['nafHeader']['id'] in ID_set:
            print("Repeated")
            pass
        else:
            cnt += 1
            # upload(document, cnt)
            print(cnt, document['nafHeader']['id'])


def change_docu():
    conn = MongoClient(host='121.40.150.141', port=27017)
    conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.Labeling_system
    coll = db.emotional_analysis_zh
    i = 0
    for docu in coll.find({}):
        i += 1
        label = '不需要'
        title = docu['nafHeader']['title']
        risk_level = interface(title)
        if risk_level == '无':
            label = '不需要'
        elif risk_level in ['高', '中', '低']:
            label = '需要'
        else:
            print('Error.')
        print(i, label, title)
        coll.update({"_id": docu['_id']}, {'$set': {"themes.0.theme":label}})


def check_content():
    conn = MongoClient(host='121.40.150.141', port=27017)
    conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.Labeling_system
    coll = db.cropus
    with open('risklevel/risk_level.json', 'w') as fo:
        cnt = 0
        for docu in coll.find({'$or':[{"taskID":13, 'cropus.themes.0.theme':'消极'},
                                      {"taskID":17, 'cropus.themes.0.theme':'需要'}]}):
            # print(docu['taskID'], docu['cropus']['themes'][0]['theme'], docu['cropus']['nafHeader']['title'])
            cnt += 1
            title = docu['cropus']['nafHeader']['title']
            content = clean_content(docu['cropus']['nafHeader']['content'])
            url = docu['cropus']['nafHeader']['url']
            if content == '':
                pass
            else:
                temp_dict = {
                    'title': title,
                    'content': content,
                    'label': '需要',
                    'url': url
                }
                fo.write(json.dumps(temp_dict, ensure_ascii=False))
                fo.write('\n')


def try_kargs(*args,**kwargs):
    for i in args:
        print(i)
    for k in kwargs:
        print(k,kwargs[k])
    pass


if __name__ == "__main__":

    # main1()
    # change_docu()
    # check_content()
    try_kargs('hello', 'world',title='title',content='content',label='label')
    pass
