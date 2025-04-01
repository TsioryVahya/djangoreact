from django.contrib import admin
from django.urls import path, include
from utilisateurs import views
from django.contrib.auth.views import LogoutView
from utilisateurs.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.after_login, name='home'),  # URL racine nommée 'home'
    path('utilisateurs/', include('utilisateurs.urls')),  # URLs de l'app utilisateurs
    path('logout/', logout_view, name='logout'),  # Add the logout URL back
    ]
