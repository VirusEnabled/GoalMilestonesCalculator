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
    return redirect('homepage')


def handler500(request, template_name=None):
    messages.error(request, f"There was an Internal Error, Try contacting your Admin.")
    return redirect('homepage')


def homepage(request):
    template = ''
    return render(request, template_name=template, context={})