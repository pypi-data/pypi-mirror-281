import sys
import os

current_dir = os.path.dirname(__file__)

if current_dir not in sys.path:
    sys.path.append(current_dir)

core_dir = os.path.join(current_dir, "core")
if core_dir not in sys.path:
    sys.path.append(current_dir)

from .core import *

#
from .ternion_commander import TernionCommander as cmd
from .ternion_monitor import TernionMonitor as mon
from .ternion_gui import TernionGui as gui

__all__ = ["tbu", "lnk", "log", "spu", "cmd", "mon", "gui"]
