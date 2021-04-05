from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from .views import *
app_name='website'

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

router = SimpleRouter()
router.register('handle_objectives', RegisterConsecutionTableViewSet, basename='handle_objectives')
router.register('interpolation_operation',InterpolationOperationViewSet,basename='interpolation_operation')

urlpatterns = \
    [
    path('',LoginUser.as_view(),name='login'),
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('logout',logout_user,name='logout'),
    path('api/', include((router.urls, 'website'))),
    path('show_objective/<int:id>/details', ObjectiveDetailView.as_view(), name='show_details'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)