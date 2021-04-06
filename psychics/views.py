import random
from django.http.response import Http404, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from .forms import CorrectAnswerForm
from edsdtest.settings import PSYCHICS_NAMES


class HomePage(View):
    template_name = 'psychics/index.html'

    def get(self, request, *args, **kwargs):
        if 'user_history' in request.session:
            user_history = request.session['user_history'].split(',')
        else:    
            user_history = []

        psychics_history = {}

        for name in PSYCHICS_NAMES:
            name_history = name + "_history"
            if name_history in request.session:
                psychics_history[name] = request.session[name_history].split(',')
            else:
                psychics_history[name] = []

        return render(request, self.template_name, {'user_history': user_history, 'psychics_history': psychics_history})



class GetGuess(View):
    form_class = CorrectAnswerForm
    template_name = 'psychics/guess.html'


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            correct_answer = request.POST['correct_answer']
            if "user_history" not in request.session:
                request.session['user_history'] = str(correct_answer)
            else:
                request.session['user_history'] = request.session['user_history'] + ",{}".format(correct_answer)
            request.session['check_performed'] = False               
            return HttpResponseRedirect(reverse('check', args=[correct_answer]))
        else:
            return render(request, self.template_name, {'form': form})


    def get(self, request, *args, **kwargs):
        if 'user_history' in request.session:
            user_history = request.session['user_history'].split(',')
        else:    
            user_history = []

        psychics_history = {}

        for name in PSYCHICS_NAMES:
            name_history = name + "_history"
            if name_history in request.session:
                psychics_history[name] = request.session[name_history].split(',')
            else:
                psychics_history[name] = []

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
        
        form = self.form_class()    

        return render(request, self.template_name, {'form': form, 'user_history': user_history, 'guesses': guesses, 'psychics_history': psychics_history})
        
    
class CheckResult(View):
    template_name = 'psychics/check.html'

    def get(self, request, correct_answer, *args, **kwargs):
        if 'user_history' in request.session:
            user_history = request.session['user_history'].split(',')
        else:    
            user_history = []

        psychics_history = {}

        for name in PSYCHICS_NAMES:
            name_history = name + "_history"
            if name_history in request.session:
                psychics_history[name] = request.session[name_history].split(',')
            else:
                psychics_history[name] = []

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
            
        return render(request, self.template_name, {'check_performed': check_performed, 'result': result, 'correct_answer': correct_answer, 
                                                    'user_history': user_history, 'psychics_history': psychics_history})



