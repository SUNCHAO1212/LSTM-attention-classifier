
from sklearn import metrics
from pymongo import MongoClient
import json

from interface import interface
from business_processing import clean_cut_sent
from main import train_predict
from business_processing import input_filter

def record_data():
    """ 记录句子、标签到 record_sent, record_label
        另外 model.py 记录了 record_prediction.txt record_attn.txt
        每次使用前删除原有文件
    """
    with open('record/record_sent', 'w') as fo1:
        with open('record/record_label', 'w') as fo2:
            with open('datasets/v2_需要_raw') as f:
                for line in f:
                    fo1.write(clean_cut_sent(line))
                    fo1.write('\n')
                    interface(line, content='测试内容')
                    fo2.write('需要')
                    fo2.write('\n')
            with open('datasets/v2_不需要_raw') as f:
                for line in f:
                    fo1.write(clean_cut_sent(line))
                    fo1.write('\n')
                    interface(line, content='测试内容')
                    fo2.write('不需要')
                    fo2.write('\n')


def confusion_matrix(y_true, y_pred):
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    precision = metrics.precision_score(y_true, y_pred, average='macro')
    recall = metrics.recall_score(y_true, y_pred, average='macro')
    f1 = metrics.f1_score(y_true, y_pred, average='weighted')

    print("confusion matrix:\n%6d\t%6d\n%6d\t%6d" % (tp, fp, fn, tn))
    print("precision: %f\nrecall: %f\nf1 score: %f" % (precision, recall, f1))
    return precision, recall, f1


def function_test():
    y_true = []
    y_pred = []
    with open('datasets/testset_需要') as f1:
        for line in f1:
            prediction = train_predict(line.strip())
            # if prediction == '需要':
            #     y_pred.append('需要')
            # elif prediction == '不需要':
            #     y_pred.append('不需要')
            # else:
            #     print('error')
            y_pred.append(prediction)
            y_true.append('需要')
    with open('datasets/testset_不需要') as f2:
        for line in f2:
            prediction = train_predict(line.strip())
            # if prediction == 'negative':
            #     y_pred.append('消极')
            # elif prediction == 'neutral':
            #     y_pred.append('中性')
            # else:
            #     print('error')
            y_pred.append(prediction)
            y_true.append('不需要')
    confusion_matrix(y_true, y_pred)


def risk_level_test():
    HOST = ['121.40.150.141', '192.168.1.251']
    PORT = 27017
    client = MongoClient(host=HOST[0], port=PORT)
    client.admin.authenticate("liangzhi", "liangzhi123$")
    db = client.Labeling_system
    coll = db.cropus
    for docu in coll.find({'taskID': 13}):  # taskID: 13, 92, 95
        label = docu['cropus']['themes'][0]['theme']
        # sent = docu['cropus']['raw']
        title = docu['cropus']['nafHeader']['title']
        content = docu['cropus']['nafHeader']['content']
        new_label = '需要' if label == '消极' else '不需要'
        risk_level = interface(title, content)
        print(risk_level, new_label, title, '\n', content)


def choose_attn_word(i):
    attn_word = []
    with open('record/record.txt') as f:
        for line in f:
            data_dict = json.loads(line.strip())
            for attn_kv in data_dict['attn_kv']:
                for k in attn_kv:
                    if attn_kv[k] > i:
                        attn_word.append(k)
    new_words = []
    for word in attn_word:
        if len(word) < 2:
            pass
        else:
            new_words.append(word)
    word_set = set(new_words)
    return word_set


def attn_test():
    i = 0
    max_dict = {
        'max_p': {
            'val': 0,
            'words': [],
            'threshold': 0
        },
        'max_r': {
            'val': 0,
            'words': [],
            'threshold': 0
        },
        'max_f': {
            'val': 0,
            'words': [],
            'threshold': 0
        },
    }
    while i < 1:
        attn_words = choose_attn_word(i)
        y_pre = []
        y_true = []
        with open('record/record.txt') as f:
            for line in f:
                data_dict = json.loads(line.strip())
                title = data_dict['sent']
                for word in attn_words:
                    if word in title:
                        y_pre.append(train_predict(title))
                        y_true.append(data_dict['label'])
                        break
                # 人工整理
                # if input_filter(title):
                #     y_pre.append(train_predict(title))
                #     y_true.append(data_dict['label'])
            precision, recall, f1 = confusion_matrix(y_true, y_pre)
            if max_dict['max_p']['val'] < precision:
                max_dict['max_p']['val'] = precision
                max_dict['max_p']['words'] = attn_words
                max_dict['max_p']['threshold'] = i
            if max_dict['max_r']['val'] < recall:
                max_dict['max_r']['val'] = recall
                max_dict['max_r']['words'] = attn_words
                max_dict['max_r']['threshold'] = i
            if max_dict['max_f']['val'] < f1:
                max_dict['max_f']['val'] = f1
                max_dict['max_f']['words'] = attn_words
                max_dict['max_f']['threshold'] = i

        print('remained: %d, threshold: %f\n' % (len(y_pre), i))
        i += 0.01
    print(max_dict)


if __name__ == '__main__':
    # record_data()  # 记录 sent/label

    function_test()
    # risk_level_test()

    # attn_test()

    # words1 = ['不过关', '修订案', '药监局', '正式', '措施', '大事记', '缺陷', '种新', '方法', '公告', '食品包装', '产品质量', '行为', '查扣', '严查', '依法查处', '合格', '饮料', '奖励', '热线', '伪劣产品', '依然', '宝坻区', '贸易', '塑料包装', '餐桌', '落实', '做出', '指南', '床垫', '开卖', '助剂', '东移', '委员', '解除', '高致病性禽流感疫情', '扶贫', '涉嫌', '小作坊', '探路', '新闻', '召回', '材料', '安全', '清单', '助鲜', 'fda', '爆红', '口岸', '白酒', '患癌', '灵芝', 'ibeile', '部门', '数据', '标准', '违反', '没收', '正在', '食物中毒', '政策', '餐饮', '拍摄', '人类', '现有']
    # words2 = []
    # with open('userfiles/attention_words_filtered') as f:
    #     for line in f:
    #         words2.append(line.strip())
    # all_words = []
    # all_words.extend(words2)
    # all_words.extend(words1)
    # print(all_words)
    # print('words1: %d\nwords2: %d\nall: %d' % (len(set(words1)), len(set(words2)), len(set(all_words))))
