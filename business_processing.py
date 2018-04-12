# -*- coding:UTF-8 -*-
# !/usr/bin/env python3

import re
import jieba
import ahocorasick
import codecs


# 清洗内容
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


# 清洗数据
digit = re.compile('[\d]+')
html = re.compile('<.+?>')
not_word = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')
space_html = re.compile('\s+')
multi_space = re.compile(' +')


def clean_data(sent):
    """ Clean sentence """
    sent = sent.strip()
    sent = html.sub('', sent)
    sent = not_word.sub(' ', sent)
    sent = space_html.sub(' ', sent)
    sent = digit.sub(' num ', sent)
    sent = sent.lower()
    sent = sent.strip()
    return sent


# 分词
jieba.load_userdict('userfiles/dict_catalog.txt')
jieba.load_userdict('userfiles/dict_entity1.txt')
jieba.load_userdict('userfiles/dict_pinpai.txt')


def cut_sent(sent):
    """ Cut sentence """
    sent = ' '.join(jieba.cut(sent))
    sent = space_html.sub(' ', sent)
    return sent


def clean_cut_sent(sent):
    return cut_sent(clean_data(sent))


# 风险等级划分（中、英）
def re_pattern(filename):
    with open(filename) as f:
        temp_list = []
        for line in f:
            temp_list.append(line.strip())
        temp_str = '|'.join(temp_list)
        temp_pattern = re.compile(temp_str)
        return temp_pattern


pattern = re_pattern('risklevel/re')
re_A = re_pattern('risklevel/A')
re_B = re_pattern('risklevel/B')
re_C = re_pattern('risklevel/C')


def chinese_risk_level(content, title, label):
    if label == '不需要':
        return '无'
    result = re.search(pattern, content)
    string = title
    if result is None:
        pass
    else:
        for i in range(len(result.regs)):
            string += result.group(i) if result.group(i) is not None else ''

    result_a = re.search(re_A, content + title)
    result_b = re.search(re_B, string)
    result_c = re.search(re_C, string)
    if result_a is not None:
        risk = '高'
    elif result_b is not None:
        risk = '中'
    elif result_c is not None:
        risk = '低'
    else:
        risk = '低'
    return risk


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
    for _ in A.iter(sent):
        return True
    return False


if __name__ == '__main__':
    """
    业务相关处理：清洗输入数据，分词，风险等级划分，筛选没有词出现在词库中的句子
    """

    # title = 'Hello Kitty警告3色蔬菜细面300克 婴儿幼儿营养面条宝宝辅食面条'
    # print(input_filter(title))

    print(chinese_risk_level('上海抽查：迪士尼宝宝、格林博士等6批次睡袋不合格','亚美尼亚阿尔卡新闻网12月7日消息，亚总理卡拉佩强在政府会议上要求有关部门加强对进出口食品的监督。卡说，尽管政府迄今为止已经做了大量工作，但食品检验还未完全采用国际标准，以致有可能导致企业对食品进出口行政管理理解不到位。他要求国家食品安全总局和经济发展及投资部年底前就食品进出口需提供文件及检验程序的若干政府决定提出修正建议。','需要'))
