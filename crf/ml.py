import pycrfsuite
from os import path


MODEL_NAME = 'crf.model'


def train(dr, train_feats, labels):
    trainer = pycrfsuite.Trainer(verbose=False)
    for x, y in zip(train_feats, labels):
        trainer.append(x, y)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 500,
        'feature.possible_transitions': True
    })

    crf_path = path.join(dr, MODEL_NAME)
    trainer.train(crf_path)


class Predictor:
    def __init__(self, dr):
        crf_path = path.join(dr, MODEL_NAME)
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(crf_path)

    def predict(self, feats):
        return self.tagger.tag(feats)
