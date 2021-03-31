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
    path('handle_objective/', handler_objective,name='handle_objective'),
    path('list_objectives/', restful_render_objectives, name='list_objectives'),
    path('delete_objective/<int:objective_id>', remove_objective, name='delete_objective'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)