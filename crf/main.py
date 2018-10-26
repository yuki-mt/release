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
words = []
not_detected = []

for sent in c.test_sents:
    tags = p.predict(sent2features(sent))
    if set(tags) == set('O'):
        not_detected.append(str(sent))
    else:
        word = ''
        is_in_word = False
        for tag, token in zip(tags, sent.to_tokens()):
            if tag.startswith('B'):
                is_in_word = True
                word += token
            elif tag.startswith('I'):
                is_in_word = True
                word += token
            elif is_in_word:
                is_in_word = False
                words.append(word)
                word = ''

with open('detected_words.txt', 'w') as f:
    f.write('\n'.join(words))

with open('not_detected.txt', 'w') as f:
    f.write('\n'.join(not_detected))
