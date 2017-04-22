from django.conf.urls import url
from django.views.generic import RedirectView

from log.forms import LoginForm

from django.contrib.auth import views as django_views
from log import views as log_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', django_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', django_views.logout, {'next_page': '/login'}),
    url(r'^register/$', log_views.register, name='register'),
]
