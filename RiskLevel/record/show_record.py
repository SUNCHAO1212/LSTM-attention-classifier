
import json
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

def record():
    """ 整合记录为 dict，每行记录一个到 record.txt
    data_dict: {
        'sent':'',
        'attn':'',
        'label':'',
        'prediction':'',
        'attn_kv':''
    }
    """
    sent_list = []
    attn_list = []
    pre_list = []
    label_list = []

    with open('record_sent') as f:
        for line in f:
            sent_list.append(line.strip())
    with open('record_attn.txt') as f:
        for line in f:
            attn_list.append(line.strip())
    with open('record_prediction.txt') as f:
        for line in f:
            pre_list.append(line.strip())
    with open('record_label') as f:
        for line in f:
            label_list.append(line.strip())

    print(len(sent_list), len(attn_list), len(pre_list), len(label_list))

    with open('record.txt', 'w') as fo:
        for i in range(len(sent_list)):
            temp_dict = {}
            temp_dict['sent'] = sent_list[i]
            temp_dict['attn'] = attn_list[i]
            temp_dict['prediction'] = pre_list[i]
            temp_dict['pre'] = '需要' if float(temp_dict['prediction'].split()[0]) > 0 else '不需要'
            temp_dict['attn_kv'] = []
            sent = sent_list[i].split()
            attn = attn_list[i].split()
            # print(sent_list[i])
            # print(attn)
            print(len(sent), len(attn))
            for j in range(len(sent)):
                # if float(attn[j]) > 0.1:
                #     # print(attn[j], sent[j])
                #     temp_dict['attn_kv'].append({attn[j]: sent[j]})
                temp_dict['attn_kv'].append({sent[j]: float(attn[j])})

            temp_dict['label'] = label_list[i]

            fo.write(json.dumps(temp_dict, ensure_ascii=False))
            fo.write('\n')


def attn_words():
    attn_word = set()
    with open('record.txt') as f:
        for line in f:
            data_dict = json.loads(line.strip())
            # print(data_dict['sent'])
            # print(data_dict['attn'])
            sent = data_dict['sent'].split()
            attn = data_dict['attn'].split()
            print(data_dict['sent'])
            for i in range(len(attn)):
                if float(attn[i]) > 0.1:
                    print(attn[i], sent[i])
                    attn_word.add(sent[i])
                else:
                    # print(attn[i])
                    pass
            # input()
    with open('attention_words', 'w') as fo:
        for i in attn_word:
            fo.write(i)
            fo.write('\n')
    print(attn_word)


if __name__ == '__main__':
    record()

    # attn_words()
