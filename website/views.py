import sys
import os
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect
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
from django.http import JsonResponse, QueryDict as qd
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import timedelta, datetime
from .helpers import *
from .models import *
from .forms import *
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
        self.request.session.set_expiry(self.request.session.get_expiry_age() * 4)
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
def logout_user(request):
    logout(request)
    messages.success(request,'Ha sido deslogueado exitosamente!')
    return redirect('website:login')


class Dashboard(TemplateView, LoginRequiredMixin):
    template_name = 'website/dashboard.html'
    redirect_field_name = 'next'
    permission_denied_message = 'Para poder acceder a esta area del sitio, debe de estar logueado'
    login_url = 'website:login'
    success_redirect = 'website:dashboard'
    extra_context = {}


    def get_context_data(self, **kwargs):
        self.extra_context['objective_form'] = ObjectiveForm(self.request.POST)
        return super().get_context_data()



