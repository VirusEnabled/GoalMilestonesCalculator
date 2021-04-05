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
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from rest_framework.parsers import JSONParser
from django.core.files import File as DF
from functools import wraps
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import timedelta, datetime
from .forms import *
from .serializers import *
from django.contrib.auth.views import LoginView
from django.views.defaults import page_not_found, server_error


def handler404(request, exception, template_name=None):
    messages.error(request, 'The page you are trying to access does not exist.')
    return redirect('login')


def handler500(request, template_name=None):
    messages.error(request, f"There was an Internal Error, Try contacting your Admin.")
    return redirect('login')

class LoginUser(LoginView):
    template_name = 'website/login.html'
    extra_context = {}
    form_class = LoginForm
    success_redirect = 'website:dashboard'

    def get_form(self,form_class=None):
        return self.form_class(self.request.POST)



    def post(self, request, *args, **kwargs):
        """
        overrides the login capabilities so that I could handle
        the messages displayed in the site
        :param request: http request
        :param args:
        :param kwargs:
        :return:
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
        form = self.get_form()
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
        return super().form_invalid(form)


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
        self.extra_context['objective_list'] = ObjectiveSerializer(instance=Objective.objects.all(),many=True).data
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


class ObjectiveDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/objective_details.html'
    model = Objective
    pk_url_kwarg = 'id'
    extra_context = {}
    login_url = 'website:login'
    permission_denied_message = "Para acceder debes de estar logueado. Por favor trate de loguearse para proseguir."
    redirect_field_name = 'next'


class RegisterConsecutionTableViewSet(ModelViewSet):
    serializer_class = ObjectiveSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = Objective.objects.all()
    objective_list_template = 'includes/responsive_table.html'

    def list(self, request, *args, **kwargs):
        payload = {'objective_list': render_to_string(self.objective_list_template,context={
            'objective_list':self.serializer_class(instance=Objective.objects.all(),many=True).data}),
                   }
        return Response(data=payload, status=status.HTTP_200_OK, content_type='application/json')


    def create(self, request, *args, **kwargs):
        """
        modifies the base class to display the proper messages
        :param request: http request
        :param args: list
        :param kwargs: dict
        :return: json response
        """
        result = {}
        st=status.HTTP_400_BAD_REQUEST
        data = request.data
        try:
            serialized = self.serializer_class(data=data)
            if serialized.is_valid():
                cleaned = serialized.validated_data
                validation = validate_goal_order(goals=[ob['goal'] for ob in cleaned['objectivegoal_set']],
                                                 consecution=[ob['consecution_percentage']
                                                              for ob in cleaned['objectivegoal_set']])
                if validation['status']:
                    serialized.save()
                    st=status.HTTP_201_CREATED
                else:
                    raise Exception(validation['error'])

            else:
                raise Exception(
                    "Hubo un problema con la informacion enviada, trate de enviarla en el formato adecuado."
                                )
        except Exception as X:
            result['error'] = f"X"

        return Response(data=result,status=st,content_type='application/json')

    def update(self, request, *args, **kwargs):
        """
        modifies the base class method to display the proper messages.
        :param request: http request
        :param args: list
        :param kwargs: dict
        :return: json response
        """
        result = {}
        st = status.HTTP_400_BAD_REQUEST
        data = request.data
        try:
            objective = Objective.objects.get(pk=self.kwargs[self.lookup_field])
            serialized = self.serializer_class(instance=objective, data=data)
            if serialized.is_valid():
                cleaned = serialized.validated_data
                validation = validate_goal_order(goals=[ob['goal'] for ob in cleaned['objectivegoal_set']],
                                                 consecution=[ob['consecution_percentage']
                                                              for ob in cleaned['objectivegoal_set']])

                if validation['status']:
                    if objective.has_consecution_calculated:
                        new_interpolation = calculate_lineal_interpolation(
                            x_new=objective.interpolationresult.interpolation,
                            x_values=[ob['goal'] for ob in cleaned['objectivegoal_set']],
                            y_values=[ob['consecution_percentage']
                                                              for ob in cleaned['objectivegoal_set']],
                            order=validation['order'])
                        objective.interpolationresult.consecution_percentage = new_interpolation
                    serialized.save()
                    objective.save()
                    st = status.HTTP_201_CREATED
                else:
                    raise Exception(validation['error'])

            else:
                raise Exception(
                    "Hubo un problema con la informacion enviada, trate de enviarla en el formato adecuado."
                )
        except Exception as X:
            result['error'] = f"{X}"

        return Response(data=result, status=st, content_type='application/json')

class InterpolationOperationViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = InterpolationResultSerializer
    permission_classes = [IsAuthenticated]
    queryset = InterpolationResult.objects.all()
    # http_method_names = ['POST','PUT']
