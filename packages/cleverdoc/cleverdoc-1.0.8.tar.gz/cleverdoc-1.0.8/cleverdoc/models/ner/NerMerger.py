
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerMerger_7aed2b9e8bc645e39ffb5d89e48d50fd.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
