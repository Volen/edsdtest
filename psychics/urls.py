  
from django.urls import path

from .views import CheckResult, GetGuess, HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('get_guess', GetGuess.as_view(), name='get_guess'),
    path('check/<int:correct_answer>', CheckResult.as_view(), name='check'),
]