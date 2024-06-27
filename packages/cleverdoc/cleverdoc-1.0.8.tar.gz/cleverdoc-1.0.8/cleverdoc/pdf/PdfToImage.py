
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfToImage_724d09cfc45d44139707272db4c05b77.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
