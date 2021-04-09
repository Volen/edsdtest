import random
from django.db import models
from django.http.response import Http404


class Psychic:
    def __init__(self, name, credibility=100):
        self.name = name
        self.credibility = credibility

    def guess_function(self):
        return random.randint(10, 99)


class PsychicsPool:
    def __init__(self, names):
        self.names = names

    def generate_guesses(self):
        guesses = {}
        for name in self.names:
            psychic = Psychic(name)
            guesses[psychic.name] = psychic.guess_function()
        return guesses    


class HistoryDB:
    def __init__(self, request):
        self.request = request

    def get_user_history(self):
        if 'user_history' in self.request.session:
            return self.request.session['user_history']
        else:
            self.request.session['user_history'] = []
            return []

    def add_correct_answer(self, correct_answer):
        if 'user_history' in self.request.session:
            self.request.session['user_history'].append(correct_answer)
        else:
            self.request.session['user_history'] = [correct_answer]


    def get_psychics_history(self, psichics_names):
        psychics_history = {}
        for name in psichics_names:
            name_history = name + "_history"
            if name_history in self.request.session:
                psychics_history[name] = self.request.session[name_history]
            else:
                self.request.session[name_history] = []
                psychics_history[name] = []
        return psychics_history

    def get_psychics_credibility(self, psichics_names):
        credibility = {}
        for name in psichics_names:
            name_credibility = name + "_credibility"
            if name_credibility in self.request.session:
                credibility[name] = self.request.session[name_credibility]
            else:
                self.request.session[name_credibility] = 100
                credibility[name] = 100
        return credibility

    def get_psychics_guesses_cache(self):
        if 'guesses' in self.request.session:
            return self.request.session['guesses']
        else:
            return {}

    def save_psychics_guesses_cache(self, guesses):
        for name, psychic_guess in guesses.items():
            name_history = name + "_history"
            self.request.session['guesses'] = guesses
            if name_history in self.request.session:                
                self.request.session[name_history].append(psychic_guess)
            else:
                self.request.session[name_history] = [psychic_guess]

    def set_check_performed(self, value):
        self.request.session['check_performed'] = value

    def get_check_perfromed(self):
        if 'check_performed' in self.request.session:
            return self.request.session['check_performed']         
        else:
            return False

    def get_final_result(self, psychics_names, correct_answer):
        result = {}
        for name in psychics_names:            
            name_history = name + "_history"
            credibility_name = name + "_credibility"
            if name_history in self.request.session:
                last_number = self.request.session[name_history][-1]
                is_correct = last_number == correct_answer
                if not credibility_name in self.request.session:
                    self.request.session[credibility_name] = 100
                if is_correct:
                    self.request.session[credibility_name] += 1
                else:    
                    self.request.session[credibility_name] -= 1
                current_credibility = self.request.session[credibility_name]
                result[name] = [is_correct, last_number, current_credibility]   
            else:
                raise Http404("Ошибка! Попробуйте сначала.")
        return result        

    def get_final_result_with_check(self, psychics_names, correct_answer):
        check_performed = self.get_check_perfromed()        
        if not check_performed:
            result = self.get_final_result(psychics_names, correct_answer)
            self.set_check_performed(True)
        else:
            result = {}
        return result    
