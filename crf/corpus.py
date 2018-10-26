import MeCab
import os
import re
from os.path import join, dirname
from dotenv import load_dotenv
from dawg import DAWG
import pickle
from models import Morpheme, Sentence
from typing import List


class CorpusReader:
    LABEL = 'corpus_label.pkl'
    TRAIN = 'corpus_train.pkl'
    TEST = 'corpus_test.pkl'

    def __init__(self,
                 train_sents: List[Sentence] = [],
                 test_sents: List[Sentence] = [],
                 labels: List[str] = []):
        self.train_sents = train_sents
        self.test_sents = test_sents
        self.labels = labels

    def save(self, dr='./'):
        with open(join(dr, self.LABEL), 'wb') as f:
            pickle.dump(self.labels, f)
        with open(join(dr, self.TRAIN), 'wb') as f:
            pickle.dump(self.train_sents, f)
        with open(join(dr, self.TEST), 'wb') as f:
            pickle.dump(self.test_sents, f)

    @classmethod
    def load(cls, dr='./'):
        with open(join(dr, cls.LABEL), 'rb') as f:
            labels = pickle.load(f)
        with open(join(dr, cls.TRAIN), 'rb') as f:
            train_sents = pickle.load(f)
        with open(join(dr, cls.TEST), 'rb') as f:
            test_sents = pickle.load(f)
        return CorpusReader(train_sents, test_sents, labels)

    def read(self, path, border):
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path)

        mecab = MeCab.Tagger("-Ochasen -u {}".format(os.environ.get("NEOLOGD_FILE")))
        mecab.parse('')
        ings = set()
        is_ings = True

        train_sents = []
        labels = []
        test_sents = []

        with open(path) as f:
            for i, line in enumerate(f):
                ing = line.strip().split('\t')[0]
                if is_ings:
                    if len(ing) < 13:  # 長すぎるentityはどうせマッチしないので追加しない
                        ings.add(ing)
                    if i == border - 1:
                        is_ings = False
                        self.dawg = DAWG(ings)
                else:
                    sent = Sentence([])
                    node = mecab.parseToNode(line)
                    while node:
                        if not node.surface:
                            node = node.next
                            continue
                        features = node.feature.split(',')
                        # 表層系、品詞1, 2と文字の種類を特徴量として追加
                        sent.append(Morpheme(node.surface,
                                    features[0],
                                    features[1],
                                    self.__get_word_type(node.surface)))
                        node = node.next
                    if sent.length == 0:
                        continue
                    label = self.__annotate(line, sent)
                    if label:
                        train_sents.append(sent)
                        labels.append(label)
                    else:
                        test_sents.append(sent)

        self.train_sents = train_sents
        self.labels = labels
        self.test_sents = test_sents

    def __get_word_type(self, word):
        if not word:
            return 'JP'
        w = word.replace('.', '')
        if not w:
            return 'SIG'
        if w.isnumeric():
            return 'NUMBER'
        if not re.sub(r'[a-zA-Z]', '', w):
            return 'ALPHA'
        if not re.sub(r'^\d+[a-zA-Z]+', '', w):
            return 'UNIT'
        if not re.sub(r'[ -~]', '', w):
            return 'SIG'
        return 'JP'

    def __annotate(self, line: str, sent: Sentence):
        # lineのどの場所がentityなのかを探す
        label_ranges = []  # type: list

        for i in range(len(line)):
            ings = self.dawg.prefixes(line[i:])
            if not ings:
                continue
            max_len = len(max(ings, key=len))
            rng = (i, i + max_len)
            new_ranges = []
            to_be_added = True
            for first, last in label_ranges:
                if rng[0] < last and rng[1] > first:
                    if last - first >= max_len:
                        new_ranges.append((first, last))
                        to_be_added = False
                else:
                    new_ranges.append((first, last))
            if to_be_added:
                new_ranges.append(rng)
            label_ranges = new_ranges

        if not label_ranges:
            return []

        # entityが見つかれば、そのsentにBIOでannotateする
        label = []
        pos = 0
        for i in range(sent.length):
            mor_last = pos + len(sent.get(i).token)
            added_to_label = False
            for first, last in label_ranges:
                if first == pos and last >= mor_last:
                    added_to_label = True
                    label.append('B-ING')
                    break
                if first < pos and last >= mor_last:
                    added_to_label = True
                    label.append('I-ING')
                    break
            if not added_to_label:
                label.append('O')
            pos = mor_last

        return label
