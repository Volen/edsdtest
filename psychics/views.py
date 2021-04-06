from django.shortcuts import render
import random

def index(request):
    return render(request, 'psychics/index.html')

def get_guess(request): 
    first = random.randint(10, 99)
    first_name = "Гуржиев"   
    second = random.randint(10, 99)
    second_name = "Угадайкин"
    request.session['first'] = first
    request.session['first_name'] = first_name    
    request.session['second'] = second
    request.session['second_name'] = second_name
    return render(request, 'psychics/guess.html')