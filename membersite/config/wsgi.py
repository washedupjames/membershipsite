"""
WSGI config for membersite project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
from pathlib import Path
#from membersite.content import *
from django.core.wsgi import get_wsgi_application





# This allows easy placement of apps within the interior
# membersite directory.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# sys.path.append(str(BASE_DIR / "membersite"))
#sys.path.insert(0, str(BASE_DIR / "membersite" / "content"))

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiply
# e sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membersite.config.settings.production")
print(os.environ["DJANGO_SETTINGS_MODULE"])
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
print("THIS IS MY WSGI")

application = get_wsgi_application()
# except Exception as e:
#     print(e)
print('WHAT NEXT AFETER WSGI')
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
