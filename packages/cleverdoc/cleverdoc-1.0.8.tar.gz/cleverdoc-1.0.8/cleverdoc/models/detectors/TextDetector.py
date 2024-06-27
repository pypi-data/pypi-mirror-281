
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'TextDetector_3d58e8f3254649e2899c42c5f25b39fb.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
