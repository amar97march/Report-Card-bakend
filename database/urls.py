from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^school/', views.SchoolApi.as_view(), name='school'),
    url(r'^getschool/(?P<school_id>[0-9]+)/$', views.SchoolApi.as_view()),
    url(r'^teacher/', views.TeacherApi.as_view(), name='teacher'),
    url(r'^getteacher/(?P<staff_id>[0-9]+)/$', views.TeacherApi.as_view()),
    url(r'^standard/', views.StandardApi.as_view(), name='standard'),
    url(r'^getstandard/(?P<div>\w+)/$', views.StandardApi.as_view()),
    url(r'^student/', views.StudentApi.as_view(), name='school'),
    url(r'^getstudent/(?P<student_id>[0-9]+)/$', views.StudentApi.as_view()),
    url(r'^reportcard/', views.ReportCardApi.as_view(), name='school'),
    url(r'^getreportcard/(?P<student_id>[0-9]+)/(?P<year>[0-9]+)/$', views.ReportCardApi.as_view()),
    url(r'^getGraph/(?P<student_id>[0-9]+)/', views.graphApi.as_view()),
]
