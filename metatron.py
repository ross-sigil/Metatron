import os
import sys

if sys.platform.startswith("linux"):
    os.system("python3 ./linux/driver.py")
else:
    print("System not compatible.")
