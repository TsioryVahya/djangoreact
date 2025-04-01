from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('accueil/', views.after_login, name='accueil'),
    path('profile/', views.profile_view, name='profile'),
    # Ne pas inclure de chemin vers 'home' ici pour éviter les conflits
    path('users/', views.user_list_view, name='user_list'),
    path('conversations/<int:user_id>/', views.get_conversation, name='get_conversation'),
    path('send-message/', views.send_message, name='send_message'),
    path('conversations/<int:conversation_id>/new-messages/<str:last_message_time>/',
         views.get_new_messages,
         name='get_new_messages'),
    path('get_all_last_messages/', views.get_all_last_messages, name='get_all_last_messages'),
]
