
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DicomToImage_8072594e59f945af8c07d0d1c1ed8c34.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
