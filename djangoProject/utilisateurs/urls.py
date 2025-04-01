from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='user_list'),
    path('conversations/<int:user_id>/', views.get_conversation, name='get_conversation'),
    path('send-message/', views.send_message, name='send_message'),
path('conversations/<int:conversation_id>/new-messages/<str:last_message_time>/',
         views.get_new_messages,
         name='get_new_messages'),
]
