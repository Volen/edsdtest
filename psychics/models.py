from django.db import models

class Psychic:

    def __init__(self, name, credibility=100):
        self.name = name
        self.credibility = credibility