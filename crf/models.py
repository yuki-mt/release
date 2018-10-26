from collections import namedtuple


Morpheme = namedtuple('Morpheme', ('token', 'pos1', 'pos2', 'type'))


class Sentence:
    def __init__(self, mors):
        self.__mors = mors

    def append(self, mor: Morpheme):
        self.__mors.append(mor)

    def __str__(self):
        return ''.join(mor.token for mor in self.__mors)

    def get(self, i):
        return self.__mors[i]

    @property
    def length(self):
        return len(self.__mors)
