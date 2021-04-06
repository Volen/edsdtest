import random
from edsdtest.settings import PSYCHICS_NAMES
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CorrectAnswerForm

def index(request):
    if 'user_history' in request.session:
        user_history = request.session['user_history'].split(',')
    else:    
        user_history = []
    return render(request, 'psychics/index.html', {'user_history': user_history})

def get_guess(request): 
    if request.method == 'POST':
        form = CorrectAnswerForm(request.POST)
        if form.is_valid():
            print(request)
            print(request.POST['correct_answer'])
            correct_answer = request.POST['correct_answer']
            if "user_history" not in request.session:
                request.session['user_history'] = str(correct_answer)
            else:
                request.session['user_history'] = request.session['user_history'] + ",{}".format(correct_answer)
            return HttpResponseRedirect(reverse('check', args=[correct_answer]))
    else:
        print(PSYCHICS_NAMES)
        if 'user_history' in request.session:
            user_history = request.session['user_history'].split(',')
        else:    
            user_history = []

        for name in PSYCHICS_NAMES:
            creability_name = name + "_credibility"
            if creability_name not in request.session:
                request.session[creability_name] = 100
        
        guesses = {}
        
        for name in PSYCHICS_NAMES:
            name_history = name + "_history"
            psychics_guess = random.randint(10, 99)
            guesses[name] = psychics_guess
            if name_history not in request.session:
                request.session[name_history] = str(psychics_guess)
            else:
                request.session[name_history] = request.session[name_history] + ",{}".format(psychics_guess)
        

        #first = random.randint(10, 99)
        #first_name = "Гурджиев"   
        #second = random.randint(10, 99)
        #second_name = "Угадайкин"
        #request.session['first'] = first
        #request.session['first_name'] = first_name    
        #request.session['second'] = second
        #request.session['second_name'] = second_name
        form = CorrectAnswerForm()    
    
    return render(request, 'psychics/guess.html', {'form': form, 'user_history': user_history, 'guesses': guesses})

def check(request, correct_answer):
    #print('Hello', correct_answer)
    #print(request.session['Гурджиев'])
    #if int(request.session['first']) != int(correct_answer):
    #    request.session['Гурджиев'] -= 1
    #else:        
    #    request.session['Гурджиев'] += 1
    #if int(request.session['second']) != int(correct_answer):
    #    request.session['Угадайкин'] -= 1
    #else:        
    #    request.session['Угадайкин'] += 1
        
    return render(request, 'psychics/check.html')