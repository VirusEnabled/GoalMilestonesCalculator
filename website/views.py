import sys
import os
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse, response as r, JsonResponse, QueryDict as qd
from django.template.loader import render_to_string
from django.template import loader
from django.views.generic import TemplateView, DetailView, ListView, RedirectView, GenericViewError
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, user_logged_in, user_logged_out
from django.contrib import messages
from rest_framework.parsers import JSONParser
from django.core.files import File as DF
from functools import wraps
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import timedelta, datetime
from .helpers import *
from .forms import *
from .serializers import ObjectiveSerializer
from django.views.defaults import page_not_found, server_error


def handler404(request, exception, template_name=None):
    messages.error(request, 'The page you are trying to access does not exist.')
    return redirect('login')


def handler500(request, template_name=None):
    messages.error(request, f"There was an Internal Error, Try contacting your Admin.")
    return redirect('login')

class LoginUser(View):
    template_name = 'website/login.html'
    extra_context = {}
    form_class = LoginForm
    success_redirect = 'website:dashboard'

    def get_form(self, request):
        """
        loads the django form
        :param request: http request
        :return: form object
        """
        return self.form_class(request.POST)

    def get(self, request):
        """
        loads the template and the form for the user
        when requested with the http GET method
        :param request:  HTTP request object
        :return: HTTP response.
        """
        if request.user.is_authenticated:
            return redirect(self.success_redirect)

        self.form = self.get_form(request)
        context = {
            'form': self.form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        validates if whether the user is worth it to pass to the site or not.
        :param request: HTTP request object
        :return: redirect
        """
        return self.validate_form(request)


    def validate_form(self, request):
        """
        validates the form is actually alright
        based on the existing matches
        :param request: http request
        :return:response if any
        """
        error = ""
        form = self.get_form(request)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(email=data['email'])
            auth  = authenticate(request, username=user, password=data['password'])
            if auth:
                return self.form_valid(form)
            error = "Correo o Contraseña incorrecta"
        return self.form_invalid(form, error=error)

    def form_valid(self, form):
        """
        processes the rest of the actions once the
        form is validated
        :param form: django form
        :return: redirect response
        """
        form_data = form.cleaned_data
        user = User.objects.get(email__exact=form_data['email'])
        login(self.request, user)
        self.request.session.set_expiry(self.request.session.get_expiry_age() * 2)
        messages.success(self.request, 'Ha sido logueado exitosamente!')
        return self.redirect_success()


    def form_invalid(self, form, error=None):
        """
        handles the error if the form is not valid
        :param form: django form
        :return: redirect response
        """
        self.extra_context['form'] = form
        messages.error(self.request,f'Hubo un error con su solicitud: '
                                    f' {[form.errors[error] for error in form.errors] if not error else error}.'
                                    f' Por favor trate de nuevo.')
        return render(self.request,self.template_name, self.extra_context)


    def redirect_success(self):
        """
        returns the user to the dashboard
        :return: http response
        """
        return redirect(self.success_redirect)


@login_required(redirect_field_name='next', login_url='website:login')
def logout_user(request:object) -> redirect:
    try:
        del request.COOKIES['authtoken']
        token = Token.objects.get(key=request.user.auth_token.key)
        token.delete()
        logout(request)

    except Exception as X:
        logout(request)

    messages.success(request, 'Ha sido deslogueado exitosamente!')
    return redirect('website:login')


class Dashboard(TemplateView, LoginRequiredMixin):
    template_name = 'website/dashboard.html'
    redirect_field_name = 'next'
    permission_denied_message = 'Para poder acceder a esta area del sitio, debe de estar logueado'
    login_url = 'website:login'
    success_redirect = 'website:dashboard'
    extra_context = {}


    def get_context_data(self, **kwargs:dict)->object:
        self.extra_context['objective_form'] = ObjectiveForm(self.request.POST)
        self.extra_context['objective_list'] =  [
                                                {'objective':obj,
                                                 'goals':[
                                                     {'goal':g.goal,
                                                      'description':g.description,
                                                      'consecution_percentage':g.consecution_percentage
                                                      }
                                                 for g in obj.objectivegoal_set.all()],
                                                    'interpolation':
                                                     {'consecution_percentage':
                                                        obj.interpolationresult.consecution_percentage,
                                                      'x_new':obj.interpolationresult.interpolation}
                                                 } for obj in Objective.objects.all()
                                                ]
        print(self.extra_context['objective_list'])
        return super().get_context_data()


    def generate_auth_cookie(self):
        """
        generates a cookie for the current logged in
        user as it needs it for the rest interaction.
        :return: str
        """
        token = Token.objects.get_or_create(user=self.request.user)[0].key
        return token


    def get(self, request:object, *args:list, **kwargs:dict) -> HttpResponse:
        """
        overrides the main get method so that
        we send the user auth token so that the user could
        use the restful methods.
        :param request: http request
        :param args: list
        :param kwargs: dict
        :return: http response object
        """
        context = self.get_context_data(**kwargs)
        context['username'] =request.user.username
        content = loader.render_to_string(self.template_name, context, request, using=None)
        response = r.HttpResponse(content=content)
        response.set_cookie('authtoken', self.generate_auth_cookie())
        return response


@api_view(http_method_names=['GET'])
def restful_render_objectives(request):
    """
    sends the existing objectives in the DB

    :param request: http request
    :return: JSON response
    """
    result = {}
    final_status = status.HTTP_400_BAD_REQUEST
    objective_list_template = 'includes/responsive_table.html'
    try:
        authenticated = validate_token(request.headers['X-AuthToken'])
        if authenticated:
            result['objective_list'] = render_to_string(objective_list_template,
                                                        context={'objective_list': [
                                                            {'objective':obj,
                                                             'goals':[
                                                                 {'goal':g.goal,
                                                                  'description':g.description,
                                                                  'consecution_percentage':g.consecution_percentage
                                                                  }
                                                             for g in obj.objectivegoal_set.all()
                                                                 ],
                                                                'interpolation':
                                                                 {'consecution_percentage':
                                                  obj.interpolationresult.consecution_percentage,
                                                                  'x_new':obj.interpolationresult.interpolation}
                                                             } for obj in Objective.objects.all()]})
            final_status = status.HTTP_200_OK
        else:
            final_status = status.HTTP_401_UNAUTHORIZED
            raise Exception("Para poder acceder a esta informacion, debe estar authenticado.")

    except Exception as X:
        result['error'] =  f"Hubo un problema con su solicitud: {X}"

    return Response(content_type='application/json', data=result, status=final_status)


@api_view(http_method_names=['POST'])
def restful_render_objective(request, objective_id):
    """
    sends the existing objectives in the DB

    :param request: http request
    :return: JSON response
    """
    data = request.data
    result = {}
    final_status = status.HTTP_400_BAD_REQUEST
    try:
        authenticated = validate_token(data['authtoken'])
        if authenticated:
            obj = Objective.objects.get(pk=objective_id)
            result['objective'] = json.dumps({'id':objective_id,
                                   'description':obj.description,
                                   'metric':obj.metric,
                                     'goals':[
                                         {'goal':g.goal,
                                          'description':g.description,
                                          'consecution_percentage':g.consecution_percentage
                                          }
                                     for g in obj.objectivegoal_set.all()
                                         ],
                                        'interpolation':
                                         {'consecution_percentage':
                          obj.interpolationresult.consecution_percentage,
                                          'x_new':obj.interpolationresult.interpolation}
                                                             })
            final_status = status.HTTP_200_OK
        else:
            final_status = status.HTTP_401_UNAUTHORIZED
            raise Exception("Para poder acceder a esta informacion, debe estar authenticado.")

    except Exception as X:
        result['error'] =  f"Hubo un problema con su solicitud: {X}"

    return Response(content_type='application/json', data=result, status=final_status)


@api_view(http_method_names=['POST'])
def handler_objective(request:object) -> Response:
    """
    creates or updates an objective based on the given params
    it must contain the following rules:
    - at least two goals
    - fields for goals and concecutions must be numbers
    - it must have the auth token for the user
    - it must have the goals setup based on the order if asc items must be asc else it will return an error
    :param request: http request
    :return: JSONResponse object
    """
    final_status = status.HTTP_400_BAD_REQUEST
    response_data = {}
    required_params = ['goals','consecution_percentages','goals_descriptions','authtoken','metric','description',
                       'new_x']
    try:
        request_data = request.data
        authenticated = validate_token(request_data['authtoken'])
        if authenticated:
            print(request_data['goals'])
            goals =[float(x) for x in request_data['goals']]
            # pdb.set_trace()
            consecution_percentages = [float(x) for x in request_data['consecution_percentages']]
            goals_descriptions =request_data['goals_descriptions']

            if len(goals) == len(consecution_percentages)== len(goals_descriptions):
                if len(goals) < 2:
                    raise Exception("Al menos debe de tener 2 metas para poder procesar el calculo.")

                values_validation = validate_goal_order(goals=goals,
                                                        consecution=consecution_percentages)
                if not values_validation['status']:
                    raise Exception(f"{values_validation['error']}")
                lineal_interpolation_result = calculate_lineal_interpolation(x_new=float(request_data['new_x']),
                                                                      y_values=consecution_percentages,
                                                                      order=values_validation['order'],
                                                                      x_values=goals)
                if 'error' not in lineal_interpolation_result.keys():
                    lineal_interpolation = lineal_interpolation_result['interpolation']
                    objective = Objective.objects.update_or_create(
                        id=int(request_data['objective_id']) if 'objective_id' in request_data.keys()\
                            else Objective.objects.last().id + 1 if Objective.objects.last() else 1,
                        description=request_data['description'],
                        metric=request_data['metric']
                    )[0]

                    for i in range(len(goals)):
                        ObjectiveGoal.objects.update_or_create(objective=objective,
                            goal=goals[i],
                            description=goals_descriptions[i],
                            consecution_percentage=consecution_percentages[i]
                        )

                    InterpolationResult.objects.update_or_create(
                        objective=objective,
                        interpolation=float(request_data['new_x']),
                        consecution_percentage=lineal_interpolation
                    )
                    final_status = status.HTTP_200_OK
                    response_data['result'] = \
                        f'El objetivo ha sido calculado y ' \
                        f'{ "actualizado" if "objective_id" in request_data.keys() else "guardado"} exitosamente!!'
                else:
                    raise Exception(f"Error-Interno: Para poder guardar los "
                                    f"registros debe haber un"
                                    f" calculo adecuado de las metricas: {lineal_interpolation_result['error']}!")
            else:
                raise Exception("Para poder procesar su informacion, "
                                "toda la informacion debe estar completa. Trate de nuevo")
        else:
            final_status = status.HTTP_401_UNAUTHORIZED
            raise Exception("Para poder acceder a esta informacion, debe estar authenticado.")

    # except KeyError:
    #     response_data['error'] = f"Hubo un error con su solicitud, debe proveer los parametros: descripcion," \
    #                              f"metrica, metas, meta, descripcion de la meta y el porcentaje de consecucion," \
    #                              f" trate de nuevo"

    except Exception as X:
        response_data['error'] = f"Hubo un error con su solicitud:{X}, trate de nuevo."

    finally:
        return Response(content_type='application/json', data=response_data, status=final_status)

@api_view(http_method_names=['POST'])
def remove_objective(request, objective_id):
    """
    sends the existing objectives in the DB
    this will take the pagination object and paginate
    the results.
    by default paginates the first page.

    :param request: http request
    :return: JSON response
    """
    result ={}
    final_status = status.HTTP_400_BAD_REQUEST
    request_data = request.data
    objective_list_template = 'includes/responsive_table.html'
    try:
        authenticated = validate_token(request_data['authtoken'])
        if authenticated:
            record = Objective.objects.get(id=objective_id)
            record.delete()
            result['message'] = 'El objetivo fue removido exitosamente!!'
            result['objective_list'] = render_to_string(objective_list_template,
                                                        context={'objective_list':Objective.objects.all()})
            final_status = status.HTTP_200_OK
        else:
            final_status = status.HTTP_401_UNAUTHORIZED
            raise Exception("Para poder acceder a esta informacion, debe estar authenticado.")

    except ObjectDoesNotExist:
        result['error'] = 'Hubo un error con el objetivo que trato de borrar, trate de nuevo.'

    except KeyError:
        result['error'] = 'Hubo un error con el objetivo que trato de borrar, trate de nuevo.'

    except Exception as E:
        result['error'] = f'Hubo un error con la solicitud {E}, trate de nuevo.'

    finally:
        return Response(content_type='application/json',data=result, status=final_status)

