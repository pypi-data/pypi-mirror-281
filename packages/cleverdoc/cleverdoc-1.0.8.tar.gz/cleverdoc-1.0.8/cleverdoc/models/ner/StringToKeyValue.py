
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'StringToKeyValue_44232b942c4049638cab73c886310032.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
