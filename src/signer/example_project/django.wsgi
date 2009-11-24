import os
import sys
sys.stdout = sys.stderr

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../")
print "ROOT_PATH: %s"%ROOT_PATH
sys.path.append(ROOT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'example_project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

