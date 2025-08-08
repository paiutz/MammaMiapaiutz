import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    try:
        os.chdir(sys._MEIPASS)
    except Exception:
        pass