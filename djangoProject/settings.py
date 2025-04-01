import os

from djangoProject.settings import BASE_DIR

# ...existing code...

# Tell Django to use your custom User model
AUTH_USER_MODEL = 'utilisateurs.User'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]