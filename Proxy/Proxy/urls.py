"""Proxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from prof_module.views import *
from stud_module.views import *
from auth_module.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', login_page),	
    url(r'^signup/$',signup),
    url(r'^login/$',login_page),
    url(r'^auth1/$',auth),
    url(r'^verify/$',before_verify),
    url(r'^verification/',after_verify),
    url(r'^finish-signup/$',finish_signup),
    url(r'^prof_home/$',prof_home),
    url(r'^prof_course/([a-zA-Z0-9]+)/$',prof_course),
    # url(r'^add_stud/([a-zA-Z0-9]+)/$',add_stud),
    url(r'^daily_report/([a-zA-Z0-9]+)/([0-9]{4})/([0-9]{2})/([0-9]{2})/$',daily_report),
    url(r'^prof_history/([a-zA-Z0-9]+)/$',prof_history),
    url(r'^take_attendance/([a-zA-Z0-9]+)/$',take_attendance),
    url(r'^upload_class_photos/([a-zA-Z0-9]+)/$',upload_class_photos),
    url(r'^prof_queries/([a-zA-Z0-9]+)/$',prof_queries),
    url(r'^query/([a-zA-Z0-9]+)/$',query),
	url(r'^stud_home/$',stud_home),
    url(r'^stud_course/([a-zA-Z0-9]+)/$',stud_course),
    url(r'^stud_daily_report/([0-9]{4})/([0-9]{2})/([0-9]{2})$',stud_daily_report),
    url(r'^stud_history/([a-zA-Z0-9]+)/$',stud_history),
    url(r'^view_queries/([a-zA-Z0-9]+)/$',view_queries),
	url(r'^raise_query/([a-zA-Z0-9]+)/$',raise_query),
	url(r'^logout/$',logout_view),
]
