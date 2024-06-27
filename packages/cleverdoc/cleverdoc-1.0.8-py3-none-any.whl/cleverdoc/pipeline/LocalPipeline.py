
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'LocalPipeline_cb1186c1a8e34284b143e07ec58b887f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
