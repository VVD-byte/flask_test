
import sys
sys.path.insert(0,"/var/www/flask_test/project")

from .project import app as application
application.secret_key = 'secret_key'