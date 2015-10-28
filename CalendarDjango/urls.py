"""CalendarDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import webcanlendar.views as views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main, name='index'),
    url(r'^(\d+)/$', views.main, name='home'),
    url(r'^month/$', views.month, name='month'),
    url(r'^month/(\d+)/(\d+)/$', views.month, name='month1'),
    url(r'^month/(\d+)/(\d+)/(prev|next)/$', views.month, name='month2'),
    url(r'^day/(\d+)/(\d+)/(\d+)/$', views.day, name='day'),
    url(r'^delete_entry/(\d+)/(\d+)/(\d+)/(\d+)/$', views.delete_entry, name='delete_entry'),
]
