import subprocess
import re
import time


print("Compilando gracias a: ZeQoSkiK")
subprocess.call("pyinstaller --onefile sick.py --icon=./sick.ico", shell=True)