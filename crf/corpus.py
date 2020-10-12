import MeCab
import os
import re
from os.path import join, dirname
from dotenv import load_dotenv
import pickle
from models import Morpheme, Sentence
from typing import List
from ahocorasick import Automaton


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
        self.__trie = None  # type: Automaton

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

    def read_entities(self, path):
        self.__trie = Automaton()
        with open(path) as f:
            for line in f:
                ing = line.strip()
                # 長すぎるentityはどうせマッチしないので追加しない
                if len(ing) < 13:
                    self.__trie.add_word(ing, len(ing))
        self.__trie.make_automaton()
        print('finish building AC Trie')

    def read_sentences(self, path, entity_path=None):
        if not self.__trie:
            self.read_entities(entity_path)

        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        mecab = MeCab.Tagger("-Ochasen -u {}".format(os.environ.get("NEOLOGD_FILE")))
        mecab.parse('')

        train_sents = []
        labels = []
        test_sents = []

        with open(path) as f:
            for line in f:
                sent = Sentence([])
                node = mecab.parseToNode(line.strip())
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
                label = self.__annotate(sent)
                if label:
                    train_sents.append(sent)
                    labels.append(label)
                else:
                    test_sents.append(sent)

        self.train_sents = train_sents
        self.labels = labels
        self.test_sents = test_sents
        print('finish reaiding file')
        print('# of train_sents: ', len(train_sents))
        print('# of test_sents: ', len(test_sents))

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

    def __get_label_range(self, sent: str):
        # どの場所がentityなのかを探す
        label_ranges = []  # type: list

        for end, length in self.__trie.iter(str(sent)):
            start = end - length + 1
            new_ranges = []
            to_be_added = True
            for l_start, l_end in label_ranges:
                # 被っていれば、長い方だけを残す
                if start < l_end and end > l_start:
                    if l_end - l_start >= end - start:
                        to_be_added = False
                    else:
                        continue
                new_ranges.append((l_start, l_end))
            if to_be_added:
                new_ranges.append((start, end))
            label_ranges = new_ranges

        return label_ranges

    def __annotate(self, sent: Sentence):
        label_ranges = self.__get_label_range(str(sent))

        if not label_ranges:
            return []

        # entityが見つかれば、そのsentにBIOでannotateする
        label = []
        mor_start = 0
        for i in range(sent.length):
            mor_end = mor_start + len(sent.get(i).token) - 1
            tag = None
            for start, end in label_ranges:
                if start == mor_start and end >= mor_end:
                    tag = 'B-ING'
                    break
                if start < mor_start and end >= mor_end:
                    tag = 'I-ING'
                    break
            if not tag:
                tag = 'O'
            label.append(tag)
            mor_start = mor_end + 1

        return label
