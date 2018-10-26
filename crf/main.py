from corpus import CorpusReader
from ml import train, Predictor
from feature import sent2features


model_dr = 'model'
c = CorpusReader()
c.read('data/corpus.txt', 1000)  # 1000行目まではentityリストが入っている
# c.save(model_dr)
# c = CorpusReader.load(dr)

train_feats = [sent2features(s) for s in c.train_sents]

train(model_dr, train_feats, c.labels)

p = Predictor(model_dr)

example_sent = c.test_sents[0]
print(example_sent)

print("Predicted:", ' '.join(p.predict(sent2features(example_sent))))
