
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.creer_client, name='creer_client'),
    path('login/', views.user_login, name='login'),
    path('log_in/', views.log_in, name='log_in'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),
    path('logout/', views.log_out, name='log_out'),
    
   

]