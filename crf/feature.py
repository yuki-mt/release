from models import Sentence


def sent2features(sent: Sentence):
    return [word2features(sent, i) for i in range(sent.length)]


def word2features(sent: Sentence, i: int):
    features = get_mor_feature(sent.get(i))
    if i >= 2:
        features.extend(get_mor_feature(sent.get(i-2), '-2'))
    else:
        features.append('BOS')

    if i >= 1:
        features.extend(get_mor_feature(sent.get(i-1), '-1'))
    else:
        features.append('BOS')

    if i < sent.length - 1:
        features.extend(get_mor_feature(sent.get(i+1), '+1'))
    else:
        features.append('EOS')

    if i < sent.length - 2:
        features.extend(get_mor_feature(sent.get(i+2), '+2'))
    else:
        features.append('EOS')

    return features


def get_mor_feature(mor, pos=None):
    features = []
    if pos is None:
        prefix = ''
        features.append('bias')
    else:
        prefix = pos + ':'

    features.extend([
        prefix + 'word=' + mor.token,
        prefix + 'pos1=' + mor.pos1,
        prefix + 'pos2=' + mor.pos2,
        prefix + 'type=' + mor.type,
    ])
    return features
