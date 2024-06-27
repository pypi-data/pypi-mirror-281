
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'OcrOutput_20cff12fa3cb45beb7b3d8261f9eb90b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
