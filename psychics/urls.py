  
from django.urls import path

from .views import index, get_guess, check

urlpatterns = [
    path('', index, name='index'),
    path('get_guess', get_guess, name='get_guess'),
    path('check/<int:correct_answer>', check, name='check'),
]