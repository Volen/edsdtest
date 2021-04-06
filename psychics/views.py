import random
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CorrectAnswerForm


def index(request):
    return render(request, 'psychics/index.html')

def get_guess(request): 
    if request.method == 'POST':
        form = CorrectAnswerForm(request.POST)
        if form.is_valid():
            print(request)
            print(request.POST['correct_answer'])
            correct_answer = request.POST['correct_answer']
            return HttpResponseRedirect(reverse('check', args=[correct_answer]))
    else:
        if "Гурджиев" not in request.session:
            request.session["Гурджиев"] = 100
        if "Угадайкин" not in request.session:
            request.session["Угадайкин"] = 100
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

def check(request, correct_answer):
    print('Hello', correct_answer)
    print(request.session['Гурджиев'])
    if int(request.session['first']) != int(correct_answer):
        request.session['Гурджиев'] -= 1
    else:        
        request.session['Гурджиев'] += 1
    if int(request.session['second']) != int(correct_answer):
        request.session['Угадайкин'] -= 1
    else:        
        request.session['Угадайкин'] += 1
        
    return render(request, 'psychics/check.html')