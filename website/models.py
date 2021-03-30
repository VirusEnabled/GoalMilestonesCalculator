from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Objective(BaseModel):
    choices = [('Descendente','DESC'),('Ascendente','ASC'),]
    description = models.CharField(max_length=150)
    metric = models.CharField(max_length=30)
    order = models.CharField(max_length=20, choices=choices, default=choices[0])


    def __str__(self):
        return f"Objetivo <{self.id}>"

class Consecution(BaseModel):
    objective = models.ForeignKey(Objective,models.CASCADE)
    goal = models.FloatField()
    description = models.CharField(max_length=30)
    consecution_percentage = models.FloatField(default=0.00)

    def __str__(self):
        return f"Consecucion <{self.goal}>"


class RenumerationResult(BaseModel):
    objective = models.OneToOneField(Objective, models.CASCADE)
    interpolation = models.FloatField(default=0.00)
