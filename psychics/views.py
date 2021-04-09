import random
from django.http.response import Http404, HttpResponseRedirect
from django.urls.base import get_urlconf
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from .forms import CorrectAnswerForm
from .models import HistoryDB, PsychicsPool
from edsdtest.settings import PSYCHICS_NAMES


class HomePage(View):
    template_name = 'psychics/index.html'

    def get(self, request):

        history_db = HistoryDB(request)
        user_history = history_db.get_user_history()
        psychics_history = history_db.get_psychics_history(PSYCHICS_NAMES)
        credibility = history_db.get_psychics_credibility(PSYCHICS_NAMES)

        return render(request, self.template_name, {'user_history': user_history, 'psychics_history': psychics_history, 
                                                    'credibility': credibility})

class GetGuess(View):
    form_class = CorrectAnswerForm
    template_name = 'psychics/guess.html'


    def post(self, request):
        form = self.form_class(request.POST)
        history_db = HistoryDB(request)
        if form.is_valid():
            correct_answer = request.POST['correct_answer']            
            history_db.add_correct_answer(correct_answer)
            request.session['check_performed'] = False
            return HttpResponseRedirect(reverse('check', args=[correct_answer]))
        else:
            user_history = history_db.get_user_history()
            psychics_history = history_db.get_psychics_history(PSYCHICS_NAMES)
            credibility = history_db.get_psychics_credibility(PSYCHICS_NAMES)
            guesses = history_db.get_psychics_guesses_cache()

            return render(request, self.template_name, {'form': form, 'user_history': user_history, 'guesses': guesses, 
                                                        'psychics_history': psychics_history, 'credibility': credibility})

    def get(self, request):

        history_db = HistoryDB(request)
        user_history = history_db.get_user_history()
        psychics_history = history_db.get_psychics_history(PSYCHICS_NAMES)
        credibility = history_db.get_psychics_credibility(PSYCHICS_NAMES)
        
        psychics_pool = PsychicsPool(PSYCHICS_NAMES)
        guesses = psychics_pool.generate_guesses()        
        history_db.save_psychics_guesses_cache(guesses)
        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'user_history': user_history, 'guesses': guesses, 
                                                    'psychics_history': psychics_history, 'credibility': credibility})
        
    
class CheckResult(View):
    template_name = 'psychics/check.html'

    def get(self, request, correct_answer):

        history_db = HistoryDB(request)
        user_history = history_db.get_user_history()
        psychics_history = history_db.get_psychics_history(PSYCHICS_NAMES)
        credibility = {}

        result = {}
        check_performed = request.session['check_performed']
        if not check_performed:
            for name in PSYCHICS_NAMES:            
                name_history = name + "_history"
                credibility_name = name + "_credibility"
                if name_history in request.session:
                    last_number = request.session[name_history][-1]
                    is_correct = last_number == correct_answer
                    if is_correct:
                        request.session[credibility_name] += 1
                    else:    
                        request.session[credibility_name] -= 1
                    current_credibility = request.session[credibility_name]
                    result[name] = [is_correct, last_number, current_credibility]   
                    credibility[name] = current_credibility
                    request.session['check_performed'] = True
                else:
                    raise Http404("Ошибка! Попробуйте сначала.")
            
        return render(request, self.template_name, {'check_performed': check_performed, 'result': result, 'correct_answer': correct_answer, 
                                                    'user_history': user_history, 'psychics_history': psychics_history, 
                                                    'credibility': credibility})



