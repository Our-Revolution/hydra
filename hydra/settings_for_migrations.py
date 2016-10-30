from .settings import *

# haaaack. don't look up tables and try to create migrations, etc.
del DATABASES['BSD']