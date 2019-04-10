"""
k交差検証をするためのサンプルコード

pip install -U pip && pip install numpy pandas pip install scikit-learn
"""

import pandas as pd
import argparse
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_recall_fscore_support


parser = argparse.ArgumentParser()
parser.add_argument('--corpus', '-c', type=str, required=True)
parser.add_argument('--split', '-s', type=int, required=True)
args = parser.parse_args()

df = pd.read_csv(args.corpus, sep='\t')
df = df.loc[df['query'].notnull(), :].ix[:, ['label', 'query']].drop_duplicates()

skf = StratifiedKFold(n_splits=args.split, shuffle=True)


# FIXME: make actual model
def train(data):
    return 'model'


n = 1
labels = []  # type: list
predicts = []  # type: list
for train_idx, test_idx in skf.split(df, df['label']):
    """ for np.array
    trains = list(ary[train_idx])
    tests = list(ary[test_idx])
    """
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    model = train(train_df)
    for index, row in df.iterrows():
        test_df['predict'] = df['query'].map(lambda q: model.predict(q))

    labels.extend(test_df['label'])
    predicts.extend(test_df['predict'])

    train_df.to_csv(f'data/{n}_th_train.txt', sep='\t', encoding='utf-8', index=False, header=False)
    test_df.to_csv('data/{}_th_test.txt'.format(n), sep='\t', encoding='utf-8', index=False)
    n += 1

# get result
uniq_labels = list(set(predicts))
precisions, recalls, f_measures, supports = \
    precision_recall_fscore_support(labels, predicts, labels=uniq_labels)

results = {}  # type: dict
for i, l in enumerate(uniq_labels):
    results[l] = {}
    results[l]["precision"] = precisions[i]
    results[l]["recall"] = recalls[i]
    results[l]["F-measure"] = f_measures[i]
    results[l]["counts"] = supports[i]

# output result
metrics = sorted(results.items(), key=lambda x: x[0])
metrics_types = sorted(m[0] for m in metrics[0][1].items())
type_order = dict((t, i) for i, t in enumerate(metrics_types))
print("Label\t{}".format("\t".join(metrics_types)))
for label, ms in metrics:
    ms = ['{:.4g}'.format(m[1]) for m in sorted(ms.items(), key=lambda _m: type_order[_m[0]])]
    print('{}\t{}'.format(label, '\t'.join(ms)))
