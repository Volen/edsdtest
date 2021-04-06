import random
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .forms import CorrectAnswerForm


def index(request):
    return render(request, 'psychics/index.html')

def get_guess(request): 
    if request.method == 'POST':
        form = CorrectAnswerForm(request.POST)
        if form.is_valid():
            print(request)
            print(request.POST['correct_answer'])
    else:
        first = random.randint(10, 99)
        first_name = "Гурджиев"   
        second = random.randint(10, 99)
        second_name = "Угадайкин"
        request.session['first'] = first
        request.session['first_name'] = first_name    
        request.session['second'] = second
        request.session['second_name'] = second_name
        form = CorrectAnswerForm()    
    
    return render(request, 'psychics/guess.html', {'form': form})