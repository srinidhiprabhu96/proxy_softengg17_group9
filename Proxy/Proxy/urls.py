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
from auth_module.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$',signup),
    url(r'^login/$',login_page),
    url(r'^auth1/$',auth),
    url(r'^verify/$',before_verify),
    url(r'^verification/',after_verify),
    url(r'^finish-signup/$',finish_signup),
    url(r'^prof_home/$',prof_home),
    url(r'^prof_course/([a-zA-Z0-9]+)/$',prof_course),
    # url(r'^add_stud/([a-zA-Z0-9]+)/$',add_stud),
    url(r'^daily_report/([a-zA-Z0-9]+)/$',daily_report),
    url(r'^prof_history/([a-zA-Z0-9]+)/$',prof_history),
    url(r'^take_attendance/([a-zA-Z0-9]+)/$',take_attendance),
    url(r'^prof_queries/$',prof_queries),
]
