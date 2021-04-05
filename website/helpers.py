from .models import *
import pdb
import json
import numpy as np


def calculate_lineal_interpolation(x_values:list,
                                   x_new: float,
                                   y_values: list,
                                   order: str) -> dict:
    """
    calculates the lineal interpolation based on the
    given params
    :param x_values: goals values
    :param x_new: new value to evaluate
    :param y_values:  values for the concecution percentages
    :param order: str: which order to calculate it to: either ASC or DESC
    :return: float: interpolation value
    """
    result = {}
    x_new = float(x_new)
    try:
        percentage_of_consecution = np.interp(x=x_new,fp=y_values, xp=x_values)
        print(x_new, min(x_values), x_values, percentage_of_consecution)
        if order == 'asc' and x_new < min(x_values):
            percentage_of_consecution = 0.00

        elif order=='asc' and x_new > max(x_values):
            percentage_of_consecution = 100.00

        elif order=='desc' and x_new > max(x_values):
            percentage_of_consecution = 0.00

        elif order=='desc' and x_new < min(x_values):
            percentage_of_consecution = 100.00
        result['interpolation'] = percentage_of_consecution

    except Exception as X:
        result['error'] = f"Hubo un error: {X}"

    return result


def validate_goal_order(goals:list, consecution:list)->dict:
    """
    validates if the given goal list is in based of the order
    :param goals: list
    :param consecution: list
    :return: bool
    5, 6,7,8,193,445 ASC
    98,33,21,10 DESC
    """
    result = {'status': False}
    if (goals and consecution) and (all(goals) and all(consecution)) and (len(goals) == len(consecution)):
        descendiente = all(goals[index] > goals[index+1] and
                             consecution[index] < consecution[index+1] for index in range(len(goals)-1))

        ascendiente = all(goals[index] < goals[index+1] and
                             consecution[index] < consecution[index+1] for index in range(len(goals)-1))
        if not descendiente and not ascendiente:
            result['error'] = "Los valores de las metas deben ser organizados de manera DESCENDIENTE o ASCENDIENTE."\
                            " Asi mismo si los valores de las metas son ASCENDIENTES,"\
                            " los porcentajes de consecucion lo deben ASCENDIENTES, si los valores de las metas son DESCENDIENTES,"\
                             " los porcentajes de consecucion debe ser ASCENDIENTES"

        elif descendiente:
            result['order'] ='desc'
            result['status'] = True

        elif ascendiente:
            result['order'] = 'asc'
            result['status'] = True
    else:
        result['error'] = "No se permiten valores vacios, " \
                          "tanto las metas como los porcentajes deben de poseer valores numericos"
    return result

def determine_consecution_percentage(goals_values: list,
                                     lineal_interpolation:float,
                                     consecution_values: list,
                                     order: str) -> float:
    """
    determines the percentage needed for the concecution based on the
    goals values, lineal interpolation and goals order
    :param goals_values: list
    :param lineal_interpolation: float
    :param order: str
    :return: float
    """

def validate_token(token: str)->bool:
    """
    validates if the token is legit
    :param token:
    :return: bool
    """
    result = False
    try:
        Token.objects.get(key=token)
        result = True

    except Exception:
        pass

    return result