
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerOutput_748ccc2b79414a61b1b1ab95bd63998d.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
