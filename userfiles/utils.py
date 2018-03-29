# # -*- utf-8 -*-
# #/usr/bin/env python3
#
# import re
# import jieba
# import json
# import os
#
# # jieba.load_userdict('dict_catalog.txt')
# # jieba.load_userdict('dict_entity1.txt')
# # jieba.load_userdict('dict_pinpai.txt')
# filtrate = re.compile(u'[^\u4E00-\u9FA5a-zA-Z0-9]')
#
#
# def cut_sent(sentence, cut_level='word'):
#     """ Clean and cut sentence """
#     # 大小写
#     sentence = re.sub('\t', '', sentence)
#     sentence = filtrate.sub(' ', sentence)
#     sentence = re.sub('[0-9]+', 'num', sentence)
#
#     if cut_level == 'word':
#         sentence = ' '.join(jieba.cut(sentence))
#     elif cut_level == 'char':
#         this_list = []
#         for word in sentence.strip():
#             this_list.append(word)
#         sentence = ' '.join(this_list)
#     else:
#         print("wrong parameter: 'cut_level'")
#
#     return sentence
#
#
# def bad_cases(sent):
#     if ('合格率' in sent and '高水平' in sent) or ('从' in sent and '删除' in sent):
#         return True
#     return False
#
#
# def risk_level(sent):
#
#     high_level = ['召回', '扣留', '违反']
#     mid_level = ['通报', '禁止', '警惕', '不合格', '超标', '不符合']
#     low_level = ['消费者警告', '监控检查', '警告']
#     void_level = ['拟修订', '修订', '拟放宽', '全部合格', '合格']
#
#     if bad_cases(sent):
#         return '无'
#
#     for word in high_level:
#         if word in sent:
#             return "高"
#     for word in mid_level:
#         if word in sent:
#             return "中"
#     for word in low_level:
#         if word in sent:
#             return "低"
#     for word in void_level:
#         if word in sent:
#             return "无"
#     # print(sent)
#
#     return "低"
#
#
# if __name__ == '__main__':
#     print("Utils")
#
