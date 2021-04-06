import random
from edsdtest.settings import PSYCHICS_NAMES
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CorrectAnswerForm

def index(request):
    if 'user_history' in request.session:
        user_history = request.session['user_history'].split(',')
    else:    
        user_history = []

    psychics_history = {}

    for name in PSYCHICS_NAMES:
        name_history = name + "_history"
        if name_history in request.session:
            psychics_history[name] = request.session[name_history]
        else:
            psychics_history[name] = []

    return render(request, 'psychics/index.html', {'user_history': user_history, 'psychics_history': psychics_history})


def get_guess(request): 
    if request.method == 'POST':
        form = CorrectAnswerForm(request.POST)
        if form.is_valid():
            correct_answer = request.POST['correct_answer']
            if "user_history" not in request.session:
                request.session['user_history'] = str(correct_answer)
            else:
                request.session['user_history'] = request.session['user_history'] + ",{}".format(correct_answer)
            request.session['check_performed'] = False               
            return HttpResponseRedirect(reverse('check', args=[correct_answer]))
    else:
        if 'user_history' in request.session:
            user_history = request.session['user_history'].split(',')
        else:    
            user_history = []

        for name in PSYCHICS_NAMES:
            name_credibility = name + "_credibility"
            if name_credibility not in request.session:
                request.session[name_credibility] = 100
        
        guesses = {}
        
        for name in PSYCHICS_NAMES:
            name_history = name + "_history"
            psychics_guess = random.randint(10, 99)
            guesses[name] = psychics_guess
            if name_history not in request.session:
                request.session[name_history] = str(psychics_guess)
            else:
                request.session[name_history] = request.session[name_history] + ",{}".format(psychics_guess)
        form = CorrectAnswerForm()    
    
    return render(request, 'psychics/guess.html', {'form': form, 'user_history': user_history, 'guesses': guesses})


def check(request, correct_answer):    
    if 'user_history' in request.session:
        user_history = request.session['user_history'].split(',')
    else:    
        user_history = []
    result = {}
    check_performed = request.session['check_performed']
    if not check_performed:
        for name in PSYCHICS_NAMES:            
            name_history = name + "_history"
            credibility_name = name + "_credibility"
            if name_history in request.session:
                last_number = int(request.session[name_history].split(',')[-1])
                is_correct = last_number == correct_answer
                if is_correct:
                    request.session[credibility_name] += 1
                else:    
                    request.session[credibility_name] -= 1
                credibility = request.session[credibility_name]
                result[name] = [is_correct, last_number, credibility]   
                request.session['check_performed'] = True
            else:
                raise Http404("Ошибка! Попробуйте сначала.")
        
    return render(request, 'psychics/check.html', {'check_performed': check_performed, 'result': result, 'correct_answer': correct_answer, 'user_history': user_history})
