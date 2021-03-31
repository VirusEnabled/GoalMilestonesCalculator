from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)



class Objective(BaseModel):
    description = models.CharField(max_length=150)
    metric = models.CharField(max_length=30)


    def __str__(self):
        return f"Objetivo <{self.id}>"

class ObjectiveGoal(BaseModel):
    objective = models.ForeignKey(Objective,models.CASCADE)
    goal = models.FloatField(default=0.00)
    description = models.CharField(max_length=30)
    consecution_percentage = models.FloatField(default=0.00)

    def __str__(self):
        return f"Meta <{self.goal}> de Objetivo <{self.objective}>"


class InterpolationResult(BaseModel):
    objective = models.OneToOneField(Objective, models.CASCADE)
    interpolation = models.FloatField(default=0.00)
    consecution_percentage = models.FloatField(default=0.00)

