from django.conf.urls import url, include
from . import views


urlpatterns = [
    url('school', views.SchoolApi.as_view(), name='school'),
    url(r'^school/(?P<school_id>\w+)/$', views.SchoolApi.as_view())    

]
