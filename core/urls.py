from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reaction-test/', views.reaction_test, name='reaction_test'),
    path('eeg-test/', views.eeg_test, name='eeg_test'),
    path('final-report/', views.final_report, name='final_report'),
    path('register/', views.register_view, name='register'),
]