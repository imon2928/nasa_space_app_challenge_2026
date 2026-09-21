from django.urls import path
from core import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('eeg-test/', views.eeg_test, name='eeg_test'),
    path('reaction-test/', views.reaction_test, name='reaction_test'),
]