# -*- coding:UTF-8 -*-
# !/usr/bin/env python

import re
import jieba
import ahocorasick
import codecs

# 清洗数据
digit = re.compile('[\d]')
html = re.compile('<.+?>')
not_word = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')
space_html = re.compile('\s+')
# valid_data = re.compile('覆盖的产品(.+?)。')

def clean_data(sent):
    """ Clean sentence """
    sent = sent.strip()
    sent = html.sub('', sent)
    sent = space_html.sub(' ', sent)
    sent = not_word.sub(' ', sent)
    sent = digit.sub('num', sent)
    sent = sent.lower()

    return sent

# 分词
jieba.load_userdict('userfiles/dict_catalog.txt')
jieba.load_userdict('userfiles/dict_entity1.txt')
jieba.load_userdict('userfiles/dict_pinpai.txt')

def cut_sent(sent):
    """ Cut sentence """
    sent = ' '.join(jieba.cut(sent))
    return sent

def clean_cut_sent(sent):
    return cut_sent(clean_data(sent))


# 风险等级划分（中、英）
high_level = ['召回', '扣留', '违反']
mid_level = ['通报', '禁止', '警惕', '不合格', '超标', '不符合']
low_level = ['消费者警告', '监控检查', '警告']
void_level = ['拟修订', '修订', '拟放宽', '全部合格', '合格']

def chinese_risk_level(sent, label):
    if label == 'negative':
        for word in high_level:
            if word in sent:
                return "高"
        for word in mid_level:
            if word in sent:
                return "中"
        # for word in low_level:
        #     if word in sent:
        #         return "低"
        for word in void_level:
            if word in sent:
                return "无"
        return "低"
    else:
        return "无"


HIGH = ['recalls', 'Recalls', 'Recall', 'Recalled', 'Hazard', 'Injury', 'Choking', 'Burn',
        'Laceration', 'Violation', 'Strangulation']
MID = ['Risk', ]
LOW = ['Alert', ]

def english_risk_level(sent):
    for high in HIGH:
        if high in sent:
            return '高'
    for mid in MID:
        if mid in sent:
            return '中'
    for low in LOW:
        if low in sent:
            return '低'
    return '无'

# AC自动机，筛选没有词在词库中的句子
A = ahocorasick.Automaton()
with codecs.open('userfiles/attention_words_filtered', 'rb', 'utf8') as f:
    for ind, l in enumerate(f.readlines()):
        l = l.strip()
        A.add_word(l, (ind, l, len(l)))
A.make_automaton()

def input_filter(sent):
    aa = A.iter(sent)
    for _ in aa:
        return True
    return False


if __name__ == '__main__':
    print("业务相关处理：清洗输入数据，分词，风险等级划分，筛选没有词出现在词库中的句子")

    title = 'Hello Kitty警告3色蔬菜细面300克 婴儿幼儿营养面条宝宝辅食面条'
    print(input_filter(title))