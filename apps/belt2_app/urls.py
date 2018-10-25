from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^addtrip$', views.addtrip),
    url(r'^deletetrip/(?P<id>\d+)$', views.deletetrip),
    url(r'^trip/(?P<id>\d+)$', views.viewtrip),
    url(r'^jointrip/(?P<id>\d+)$', views.join),
    url(r'^leavetrip/(?P<id>\d+)$', views.leave),
]
