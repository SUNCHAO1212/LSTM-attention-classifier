
from sklearn import metrics

from interface import interface
from business_processing import clean_cut_sent
from main import train_predict


def record_data():
    """ 记录句子、标签到 record_sent, record_label
        另外 model.py 记录了 record_prediction.txt record_attn.txt
        每次使用前删除原有文件
    """
    with open('record/record_sent', 'w') as fo1:
        with open('record/record_label', 'w') as fo2:
            with open('datasets/消极') as f:
                for line in f:
                    fo1.write(clean_cut_sent((line)))
                    fo1.write('\n')
                    risk_level = interface(line)
                    if risk_level in ['高', '中', '低']:
                        fo2.write('负')
                    else:
                        fo2.write('中')
                    fo2.write('\n')
            with open('datasets/中性') as f:
                for line in f:
                    fo1.write(clean_cut_sent(line))
                    fo1.write('\n')
                    risk_level = interface(line)
                    if risk_level in ['高', '中', '低']:
                        fo2.write('负')
                    else:
                        fo2.write('中')
                    fo2.write('\n')


def function_test():
    y_true = []
    y_pred = []
    with open('datasets/消极情感') as f1:
        for line in f1:
            prediction = train_predict(line.strip())
            if prediction == 'negative':
                y_pred.append('消极')
            elif prediction == 'neutral':
                y_pred.append('中性')
            else:
                print('error')
            y_true.append('消极')
    with open('datasets/中性情感') as f2:
        for line in f2:
            prediction = train_predict(line.strip())
            if prediction == 'negative':
                y_pred.append('消极')
            elif prediction == 'neutral':
                y_pred.append('中性')
            else:
                print('error')
            y_true.append('中性')
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    precision = metrics.precision_score(y_true, y_pred, average='macro')
    recall = metrics.recall_score(y_true, y_pred, average='macro')
    f1 = metrics.f1_score(y_true, y_pred, average='weighted')
    kappa_score = metrics.cohen_kappa_score(y_true, y_pred)
    # roc = metrics.roc_auc_score(y_true, y_pred)

    print("confusion matrix:\n%6d\t%6d\n%6d\t%6d" % (tp, fp, fn, tn))
    print("precision: %f\nrecall: %f\nf1 score: %f\nkappa score: %f\n" % (precision, recall, f1, kappa_score))


if __name__ == '__main__':
    # record_data()  # 记录 sent/label
    function_test()
