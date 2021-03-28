from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class Objective(models.Model):
    description = models.CharField(max_length=150)
    metric = models.CharField(max_length=30)


    def __str__(self):
        return f"Objetivo <{self.id}>"

class Consecution(models.Model):
    objective = models.ForeignKey(Objective,models.CASCADE)
    goal = models.FloatField()
    description = models.CharField(max_length=30)
    consecution_percentage = models.FloatField()

    def __str__(self):
        return f"Consecucion <{self.goal}>"


class RenumerationResult(models.Model):
    pass