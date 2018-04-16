# For interface user
Check main.py. Cancel comment of these two line:
```
args.snapshot = "./risklevel/snapshot/2018-03-11_20-00-14/best_steps_1500.pt"
args.predict = "开启预测流程，取消注释后可调用，注释后可进行训练"
```
## 使用说明
这是一个风险预警模型，使用LSTM+attention。模型为二分类器：消极、中性（暂定名称）。
风险等级现在使用人工规则，具体可在business_processing.py查看。
训练集选择、分类选择在mydatasets.py中查看。
在main.py中进行训练，将一下两行注释后运行即可：
```
args.snapshot = "./risklevel/snapshot/2018-03-11_20-00-14/best_steps_1500.pt"
args.predict = "开启预测流程，取消注释后可调用，注释后可进行训练"
```
预测时，将以上两行取消注释，并在 "snapshot" 文件夹下选择模型进行预测，接口在interface.py中。
其他跟业务相关的设置在business_processing.py中，包括风险等级、分词方式选择、中英文处理等。
