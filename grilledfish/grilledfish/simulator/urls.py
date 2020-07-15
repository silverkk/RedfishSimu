from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^v1/.*$', views.redfish_v1, name='redfish_v1'),
    re_path(r'^control/health.*$', views.redfish_health_control, name='redfish_control'),
    re_path(r'^control/perf.*$', views.redfish_perf_summary, name='redfish_perf'),    
    re_path(r'^.*$', views.web_request, name='web_request'),
]
