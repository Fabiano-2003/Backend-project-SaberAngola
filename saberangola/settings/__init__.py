from .base import *

# Import environment-specific settings
import os
from decouple import config

env = config('DJANGO_ENV', default='dev')

if env == 'production':
    from .prod import *
else:
    from .dev import *