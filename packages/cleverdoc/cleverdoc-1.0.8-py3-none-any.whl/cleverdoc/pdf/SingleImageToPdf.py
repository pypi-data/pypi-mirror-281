
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'SingleImageToPdf_496422b2e99941d5a2c1dac45a76601f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
