
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'enums_1be7c1e22be34c72b0eb61f1f963f709.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
