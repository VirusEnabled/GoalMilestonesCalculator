from rest_framework.serializers import ModelSerializer
import pdb
from .helpers import *



class ObjectiveGoalSerializer(ModelSerializer):
    class Meta:
        model = ObjectiveGoal
        fields = ['objective','description','goal', 'consecution_percentage']
        depth = 1


class InterpolationResultSerializer(ModelSerializer):
    class Meta:
        model=InterpolationResult
        fields = ['objective','interpolation','consecution_percentage']
        depth=1

    def is_valid(self, raise_exception=False):
        """
        here we modify the behavior
        to add better functionality
        :param raise_exception: Exception to raise if not valid
        :return: bool
        """
        self.objective = Objective.objects.get(pk=self.initial_data['objective'])
        return super().is_valid(raise_exception)


    def create(self, validated_data):
        """
        overriding the creating method so that
        we make sure there's good info
        :param validated_data:
        :return:
        """
        x_values = [ob.goal for ob in self.objective.objectivegoal_set.all()]
        y_values = [ob.consecution_percentage for ob in self.objective.objectivegoal_set.all()]
        order = validate_goal_order(goals=x_values,
                                    consecution=y_values)
        if order['status']:
            interpolation = calculate_lineal_interpolation(x_values=x_values,y_values=y_values,order=order['order'],
                                                           x_new=validated_data['interpolation'])
            instance = InterpolationResult.objects.create(objective=self.objective,
                                                          interpolation=validated_data['interpolation'],
                                                          consecution_percentage=interpolation['interpolation'])
            return instance
        else:
            raise AttributeError(order['error'])

    def update(self, instance, validated_data):
        """
        updates an existing value
        :param instance:
        :param validated_data:
        :return:
        """
        x_values = [ob.goal for ob in self.objective.objectivegoal_set.all()]
        y_values = [ob.consecution_percentage for ob in self.objective.objectivegoal_set.all()]
        order = validate_goal_order(goals=x_values,
                                    consecution=y_values)
        if order['status']:
            interpolation = calculate_lineal_interpolation(x_values=x_values, y_values=y_values, order=order['order'],
                                                           x_new=validated_data['interpolation'])
            instance.interpolation =validated_data['interpolation']
            instance.consecution_percentage=interpolation['interpolation']
            instance.save()
            return instance
        else:
            raise AttributeError(order['error'])

class ObjectiveSerializer(ModelSerializer):
    objectivegoal_set = ObjectiveGoalSerializer(many=True)
    interpolationresult = InterpolationResult()

    class Meta:
        model = Objective
        fields  = ['id',
                   'metric',
                   'description',
                   'objectivegoal_set',
                   'interpolationresult'
                   ]
        depth = 1


    def is_valid(self, raise_exception=False):
        """
        here we modify the behavior
        to add better functionality
        :param raise_exception: Exception to raise if not valid
        :return: bool
        """
        return super().is_valid(raise_exception)


    def create(self, validated_data):
        """
        modified methods
        :param validated_data:
        :return: django model instance
        """
        goals = validated_data.pop('objectivegoal_set')
        obj = Objective.objects.create(**validated_data)
        for goal in goals:
            ObjectiveGoal.objects.create(objective=obj,**goal)
        return obj

    def update(self, instance, validated_data):
        """
        modified methods
        :param instance: Objective's data
        :param validated_data: dict
        :return:django model instance
        """
        # pdb.set_trace()
        goals = validated_data.pop('objectivegoal_set')
        instance.metric = validated_data['metric']
        instance.description = validated_data['description']
        instance.save()
        for goal in goals:
            ObjectiveGoal.objects.update_or_create(objective=instance, **goal)
        return instance