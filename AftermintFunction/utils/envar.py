import os

def getEnvironmentVariable(name):
    try:
        return os.environ[name]
    except:
        return ''