

from pymongo import MongoClient
from risklevel.main import train_predict

from risklevel.business_processing import *


def interface(sent, content, flag='zh'):
    """
    :param sent: the title of document
    :param content: the content of document
    :param flag: language flag, 'zh'(Chinese) or 'en'(English)
    :return: risk_level:'高', '中', '低', '无'
    """
    if flag == 'zh':
        # if input_filter(sent):
        #     pass
        # else:
        #     return '无'
        label = train_predict(clean_cut_sent(sent))  # negative, neutral
        risk_level = chinese_risk_level(sent, content, label)
    elif flag == 'en':
        risk_level = english_risk_level(sent)
    else:
        print("Please check language flag")
        risk_level = '无'
    return risk_level


if __name__ == '__main__':

    print(interface('上海抽查：迪士尼宝宝、格林博士等6批次睡袋不合格','亚美尼亚阿尔卡新闻网12月7日消息，亚总理卡拉佩强在政府会议上要求有关部门加强对进出口食品的监督。卡说，尽管政府迄今为止已经做了大量工作，但食品检验还未完全采用国际标准，以致有可能导致企业对食品进出口行政管理理解不到位,存在安全隐患。他要求国家食品安全总局和经济发展及投资部年底前就食品进出口需提供文件及检验程序的若干政府决定提出修正建议。'))
