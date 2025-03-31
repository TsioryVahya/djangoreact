from django.contrib import admin
from django.urls import path, include
from utilisateurs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.after_login, name='home'),  # URL racine nommée 'home'
    path('utilisateurs/', include('utilisateurs.urls')),  # URLs de l'app utilisateurs
]
