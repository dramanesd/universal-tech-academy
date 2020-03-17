import os
class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or b',N\xd1\xef\xf3\x9cS\xcb\x98\x16m\r9\xc18\xab'
  
  MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }