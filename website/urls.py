from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import BaseRouter
from .views import *
app_name='website'

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = \
    [
    path('',LoginUser.as_view(),name='login'),
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('logout',logout_user,name='logout'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)