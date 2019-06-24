"""
各ラベルのデータがどのラベルデータに分類されたかをヒートマップで表現する

pip install -U pip && pip install numpy pandas seaborn
"""
import numpy as np
import pandas as pd
import seaborn as sns


classes = ['label_A', 'label_B', 'label_C']

heatmap = np.zeros((len(classes), len(classes)), dtype=np.float)


# TODO
def predict(data):
    # [label_Aの確率, label_Bの確率 label_Cの確率]
    return np.array([0.8, 0.4, 0.2])


for index, name in enumerate(classes):
    print(name)
    total = 0
    with open("data/{}.tsv".format(name)) as infile:
        for line in infile:
            total += 1
            label, data = line.strip().split('\t')
            heatmap[index] += predict(data)
    heatmap[index] /= total


# 縦軸: 実際のカテゴリ, 横軸: 予想カテゴリ
df = pd.DataFrame(heatmap, columns=classes, index=classes)
sns.heatmap(df, annot=True, fmt="0.2f")
