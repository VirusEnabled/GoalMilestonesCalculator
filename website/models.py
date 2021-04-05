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


    @property
    def has_consecution_calculated(self):
        """
        verifies if the objective itself has been
        calculated already.
        :return:
        """
        result = False
        try:
            x = self.interpolationresult.interpolation
            result = True
        except Exception:
            pass
        return result

    @property
    def max_consecution(self):
        """
        gets the maximum consecution percentage
        :return:float if exists else none
        """
        cons = self.objectivegoal_set.all()
        return max(obj.consecution_percentage
                   for obj in cons) if cons else None

    @property
    def min_consecution(self):
        """
        gets the minimun consecution
        value
        :return:float if exists else none
        """
        cons = self.objectivegoal_set.all()
        return min(obj.consecution_percentage
                   for obj in cons) if cons else None

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

