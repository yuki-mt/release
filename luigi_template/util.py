"""
Luigiの雛形。task2.txtがあるときは内容変えてrunしても何も起こらない

e.g.
python luigi_test.py -f --flt 4.51 --str-prm yeah!
"""
import luigi
import sys
from abc import ABCMeta, abstractmethod
from typing import Union


class BaseTask(luigi.Task, metaclass=ABCMeta):
    # Overwrite if needed
    path = ''
    delete_input_file = True

    @abstractmethod
    def _run(self, input_data: Union[str, None], target):
        pass

    def run(self):
        # 依存先のoutputがあるかどうか
        if self.input():
            with self.input().open("r") as intermediate, self.output().open("w") as target:
                self._run(intermediate.read(), target)
            if self.delete_input_file:
                self.input().remove()
        else:
            with self.output().open("w") as target:
                self._run(None, target)

    def output(self):
        path = self.path if self.path else self.__class__.__name__ + '.txt'
        return luigi.LocalTarget(path)


# 一旦止めて、問題ないなら続行
class AskTask(luigi.Task):
    # Overwrite if needed
    delete_input_file = True
    delete_input_file_when_exit = False

    def run(self):
        is_continue = input('OK to keep going?: ([Y]/n)').lower() in ['yes', 'y', '']
        if not is_continue:
            sys.exit(0)
            if self.delete_input_file_when_exit:
                self.input().remove()

        with self.input().open("r") as intermediate, self.output().open("w") as target:
            target.write(intermediate.read())

        if self.delete_input_file:
            self.input().remove()

    def output(self):
        path = self.__class__.__name__ + '.txt'
        return luigi.LocalTarget(path)
