"""
各ラベルのデータがどのラベルデータに分類されたかをヒートマップで表現する
"""
import sys
from itertools import chain


def find_huge_vars(threshold_bytes: int, variables=None):
    def compute_object_size(o):
        def dict_handler(d):
            return chain.from_iterable(d.items())
        all_handlers = {tuple: iter, list: iter, dict: dict_handler, set: iter}
        seen = set()
        default_size = sys.getsizeof(0)

        def sizeof(o):
            if id(o) in seen:
                return 0
            seen.add(id(o))
            s = sys.getsizeof(o, default_size)
            for typ, handler in all_handlers.items():
                if isinstance(o, typ):
                    s += sum(map(sizeof, handler(o)))
                    break
            return s
        return sizeof(o)

    variables = variables if variables else globals().copy()
    for k, v in variables.items():
        if hasattr(v, '__dict__'):
            size = compute_object_size(dict(v.__dict__))
        else:
            size = compute_object_size(v)
        if size > threshold_bytes:
            print('name: {}, size: {:.3f} MB'.format(k, size / (1000 * 1000)))


# sample global vars

class A:
    f = 'ffffffffffff' * 10000

    def __init__(self):
        self.b = 'b' * 1000000


lis = ['lis'] * 100000
x = A()


def main():
    a = 'few' * 1000000
    print('find global vars')
    find_huge_vars(100 * 1000)  # 100KB
    print('find local vars')
    find_huge_vars(100 * 1000, locals())  # 100KB


if __name__ == '__main__':
    main()
