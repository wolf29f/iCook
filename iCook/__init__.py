import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from . import Frame
from . import DataBase
from . import Recipe
app = Frame.MainFrame.MainFrame()