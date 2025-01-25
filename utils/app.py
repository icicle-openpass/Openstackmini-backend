from flask import Flask
import socket
import platform
import os

# Check OS
os_name = platform.system()
hostname = socket.gethostname()
if os_name == "Darwin":
    app = Flask(__name__)
elif os_name == "Linux":
    app = Flask(__name__)
elif os_name == "Windows":
    print("OS not Supported")
else:
    print("OS not Supported")