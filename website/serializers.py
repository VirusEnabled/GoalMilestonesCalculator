from rest_framework.serializers import ModelSerializer

from .models import *



class ObjectiveSerializer(ModelSerializer):
    class Meta:
        model = Objective
        fields  = ['id','metric','description','objectivegoal_set','interpolationresult']