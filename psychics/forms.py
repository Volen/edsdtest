from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 

class CorrectAnswerForm(forms.Form):
    correct_answer = forms.IntegerField(label='Загаданное число', validators=[MinValueValidator(10), MaxValueValidator(99)])