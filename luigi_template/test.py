"""
Luigiの雛形。task2.txtがあるときは内容変えてrunしても何も起こらない

e.g.
python luigi_test.py -f --flt 4.51 --str-prm yeah!
"""
import luigi
import sys
import os
from util import BaseTask, AskTask
from typing import Union


class Task1(BaseTask):
    param = luigi.BoolParameter()

    def _run(self, input_data: Union[str, None], target):
        target.write(f"passed bool param {self.param}.")


class MyAskTask(AskTask):
    param = luigi.BoolParameter()

    def requires(self):
        return Task1(param=self.param)


class Task2(BaseTask):
    path = 'text2.txt'
    integer = luigi.IntParameter(default=10)
    flt = luigi.FloatParameter()
    str_prm = luigi.Parameter()

    def requires(self):
        return MyAskTask(param=self.integer + self.flt > 15)

    def _run(self, input_data: Union[str, None], target):
        target.write(f"{input_data}\n")
        target.write(f"I am task2. param = {self.str_prm}")


if __name__ == '__main__':
    if '-f' in sys.argv:
        if os.path.exists(Task2.path):
            os.remove(Task2.path)
        sys.argv.remove('-f')

    luigi.run(['Task2', '--workers', '1', '--local-scheduler'] + sys.argv[1:])
