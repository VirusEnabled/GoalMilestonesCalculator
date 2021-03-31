from .models import *
import pdb
import json
import numpy as np

def linear_interpolation_asc(x_new, data):
    """
    calculates the lineal interpolation in an asc order
    :param x_new: new x to be using
    :param data: consecution percentages
    :return: float
    """
    j = 0
    while (data[j][0] < x_new and data[j+1][0] < x_new):
        j = j + 1
    x_left = data[j][0]
    x_right = data[j+1][0]
    y_left = data[j][1]
    y_right = data[j+1][1]

    slope = (y_right-y_left)/(x_right-x_left)
    intercept = y_left-slope*x_left
    y_new = slope*x_new+intercept

    return y_new


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
    try:
        if x_new < min(x_values) or x_new > max(x_values):
            result['error'] = f"El valor proveido {x_new} es invalido para poder calcular la interpolacion. porfavor provea " \
                              f"valores dentro del rango:{min(x_values)} -{max(x_values)}"
        else:
            # percentage_of_consecution = np.interp(xp=x_new,x=x_values,fp=y_values)
            percentage_of_consecution = linear_interpolation_asc(x_new=x_new,data=[x_values,y_values])

            if order=='asc' and percentage_of_consecution < min(x_values):
                percentage_of_consecution = 0.00

            elif order=='asc' and percentage_of_consecution < max(x_values):
                percentage_of_consecution = 100.00

            elif order=='desc' and percentage_of_consecution > max(x_values):
                percentage_of_consecution = 0.00

            elif order=='desc' and percentage_of_consecution < min(x_values):
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