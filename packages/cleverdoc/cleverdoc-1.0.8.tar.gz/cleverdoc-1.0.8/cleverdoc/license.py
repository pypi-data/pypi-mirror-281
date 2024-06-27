
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'license_a16b6cfceaec4e4db75393819cdfe7b6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
