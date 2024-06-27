import ctypes
import os

class BlueScreenDLL:
    def __init__(self, dll_filename="bst.dll"):
        current_dir = os.path.dirname(__file__)
        self.dll_path = os.path.join(current_dir, dll_filename)

    def start(self):
        dll = ctypes.CDLL(self.dll_path)
        dll.start.argtypes = []
        dll.start.restype = None
        dll.start()

def start():
    blue_screen = BlueScreenDLL()
    blue_screen.start()
