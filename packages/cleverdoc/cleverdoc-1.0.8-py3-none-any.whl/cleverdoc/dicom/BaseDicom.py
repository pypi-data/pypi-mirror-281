
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BaseDicom_ae8f618b44ac4ebc9a318e7d91e9a685.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
