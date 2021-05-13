import os

try:
    os.remove("../test.db")
except FileNotFoundError:
    pass
