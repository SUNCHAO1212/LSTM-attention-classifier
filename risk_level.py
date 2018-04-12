# -*- coding:UTF-8 -*-
#!/usr/bin/env python3

import re
import json
from pymongo import MongoClient


def re_pattern(filename):
    with open(filename) as f:
        temp_list = []
        for line in f:
            temp_list.append(line.strip())
        temp_str = '|'.join(temp_list)
        pattern = re.compile(temp_str)
        return pattern
pattern = re_pattern('risklevel/re')
A = re_pattern('risklevel/A')
B = re_pattern('risklevel/B')
C = re_pattern('risklevel/C')


def risk_level(string, title, cnt_dict):
    result = re.search(pattern, string)
    new_string = title
    if result is None:
        # new_string = string
        # print('-' * 50, '\n', new_string)
        pass
    else:
        for i in range(len(result.regs)):
            new_string += result.group(i) if result.group(i) is not None else ''
        # print('%')

    result_a = re.search(A, string + title)
    result_b = re.search(B, new_string)
    result_c = re.search(C, new_string)
    if result_a is not None:
        # print('A')
        with open('risklevel/risk_a.json', 'a') as fo:
            temp_dict = {
                'content': string,
                'title': title,
                'risk': 'A'
            }
            fo.write(json.dumps(temp_dict, ensure_ascii=False))
            fo.write('\n')
        cnt_dict['a'] += 1
    elif result_b is not None:
        # print('B')
        with open('risklevel/risk_b.json', 'a') as fo:
            temp_dict = {
                'content': new_string,
                'title': title,
                'risk': 'B'
            }
            fo.write(json.dumps(temp_dict, ensure_ascii=False))
            fo.write('\n')
        cnt_dict['b'] += 1
    elif result_c is not None:
        # print('C')
        with open('risklevel/risk_c.json', 'a') as fo:
            temp_dict = {
                'content': new_string,
                'title': title,
                'risk': 'C'
            }
            fo.write(json.dumps(temp_dict, ensure_ascii=False))
            fo.write('\n')
        cnt_dict['c'] += 1
    else:
        with open('risklevel/risk_no.json', 'a') as fo:
            temp_dict = {
                'content': new_string,
                'title': title,
                'risk': 'NO'
            }
            fo.write(json.dumps(temp_dict, ensure_ascii=False))
            fo.write('\n')
        cnt_dict['no'] += 1
        # print('-'*50, '\n', new_string)


if __name__ == '__main__':
    conn = MongoClient(host='121.40.150.141', port=27017)
    conn.admin.authenticate("liangzhi", "liangzhi123$")
    db = conn.Labeling_system
    coll = db.cropus

    cnt = 0
    cnt_dict = {
        'a': 0,
        'b': 0,
        'c': 0,
        'no': 0,
    }
    for docu in coll.find({'$or': [{"taskID": 13, 'cropus.themes.0.theme': '消极'},
                                   {"taskID": 17, 'cropus.themes.0.theme': '需要'}]}):
        # print(docu['taskID'], docu['cropus']['themes'][0]['theme'], docu['cropus']['nafHeader']['title'])
        content = docu['cropus']['nafHeader']['content']
        title = docu['cropus']['nafHeader']['title']
        cnt += 1

        risk_level(content, title, cnt_dict)
    print(cnt)
    print(cnt_dict)
