import os
import sys

filename = __file__

directory = os.path.dirname(filename)

project_root = os.path.join(directory,'..')

sys.path.insert(0,project_root)