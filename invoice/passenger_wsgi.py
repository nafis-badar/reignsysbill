import os
import sys

sys.path.insert(0,os.path.dirname(__file__))

def application(environ,start_response):
    start_response('200 ok',[('Content-Type','text/plain')])
    message = "it works\n"
    version = 'Python %s' %sys.version.split()[0]
    response = '\n'.join([message,version])
    return [response.encode()]