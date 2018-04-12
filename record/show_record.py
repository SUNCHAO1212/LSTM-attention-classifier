
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


def get_confusion_matrix():
    """confusion_matrix api: http://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html"""
    max_pre_1, min_pre_1, max_pre_2, min_pre_2 = 10, -10, 10, -10
    step = 0.01
    threshold = min_pre_1
    confusion_matrix_dict = {
        'matrix_order': 'tn, fp, fn, tp',
        'matrix': [],
        'threshold': []
    }
    while threshold < max_pre_1:
        pre_list = []
        label_list = []

        # pre_1 = []
        with open('record.txt') as f:
            for line in f:
                data_dict = json.loads(line.strip())
                pre = float(data_dict['prediction'].split()[0])
                if pre > threshold:
                    pre_label = '负'
                else:
                    pre_label = '中'
                pre_list.append(pre_label)
                label_list.append(data_dict['label'])
        #         max_pre_1 = max(max_pre_1, pre)
        #         min_pre_1 = min(min_pre_1, pre)
        #         max_pre_2 = max(max_pre_2, float(data_dict['prediction'].split()[1]))
        #         min_pre_2 = min(min_pre_2, float(data_dict['prediction'].split()[1]))
        #         pre_1.append(float(data_dict['prediction'].split()[0]))
        # a = np.array(pre_1)
        # quantile = np.percentile(a, 66)
        # print('quantile = %f' % quantile)

        tn, fp, fn, tp = confusion_matrix(label_list, pre_list).ravel()
        confusion_matrix_dict['matrix'].append([tn, fp, fn, tp])
        confusion_matrix_dict['threshold'].append(threshold)
        print('threshold: %f' % threshold)
        print(tp, '\t', fp, '\n', fn, '\t', tn)
        threshold += step

    # print('-'*50, '\n', max_pre_1, min_pre_1, max_pre_2, min_pre_2)
    fc2(confusion_matrix_dict)


def fc2(input_dict, quantile=0.94):
    """
    ROC curve, PR curve.
    'matrix_order': 'tn, fp, fn, tp'
    :param input_dict:
    :return:
    """
    print('Matrix order: ', input_dict['matrix_order'])
    tpr = []
    fpr = []
    precision = []
    recall = []
    for i in input_dict['matrix']:
        tn = i[0]
        fp = i[1]
        fn = i[2]
        tp = i[3]
        tpr.append(tp/(tp+fn))
        fpr.append(fp/(tn+fp))
        precision.append(tp/(tp+fp))
        recall.append(tp/(tp+fn))

    plt.plot(fpr, tpr, 'k--', label='ROC(threshold = %f)' % quantile, lw=1)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    # plt.savefig("ROC.jpg")
    plt.show()

    plt.plot(recall, precision, label='PR(threshold = %f)' % quantile, lw=1)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('PR curve')
    plt.legend(loc="lower right")
    # plt.savefig("PR.jpg")
    plt.show()


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

    # result_list = result_list()
    # draw(result_list)

    # get_confusion_matrix()

    # attn_words()
