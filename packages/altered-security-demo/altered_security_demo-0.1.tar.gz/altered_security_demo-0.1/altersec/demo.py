import os
import ctypes

def demo_function():
    ctypes.windll.user32.MessageBoxW(0, "Free malware hosting by PyPi", "Message", 1)
    os.system("calc.exe")
