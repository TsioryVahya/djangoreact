# ...existing code...

# Tell Django to use your custom User model
AUTH_USER_MODEL = 'utilisateurs.User'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'accueil'
LOGOUT_REDIRECT_URL = 'login'

# ...existing code...