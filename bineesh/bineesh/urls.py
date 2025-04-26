from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('Schedule/', views.Schedule, name='Schedule'),
    path('freeTrialModal/', views.freeTrialModal, name='freeTrialModal'),
    
    path('enroll/', views.enroll, name='enroll'),
    path('Instructors/', views.Instructors, name='Instructors'),
    
    # Add other paths as needed
    
]