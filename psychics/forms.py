from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 

class CorrectAnswerForm(forms.Form):
    correct_answer = forms.PositiveIntgerField(label='Загаданное число', default=10, validators=[MinValueValidator(10), MaxValueValidator(99)])