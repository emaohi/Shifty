from django.conf.urls import url

from log.forms import LoginForm

from django.contrib.auth import views as django_views
from log import views as log_views
from . import views

urlpatterns = [

    # url(r'^home/$', views.home, name='real_home'),
    url(r'^$', views.home_or_login, name='home'),
    url(r'^login_success$', views.login_success, name='login_success'),
    url(r'^login/$', django_views.login, {'template_name': 'login.html',
                                          'authentication_form': LoginForm}, name='login'),
    url(r'^register/$', log_views.register, name='register'),
    url(r'^success/$', views.success, name='success'),
    url(r'^logout/$', django_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^edit_profile/$', django_views.logout, {'next_page': 'login'}, name='logout'),
    # -------------- Manager section ------------------------ #

    url(r'^manager/$', views.manager_home, name='manager_home'),
    url(r'^manager/logout/$', django_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^manager/edit_business/$', views.edit_business, name='edit_business'),
    url(r'^manager/add_employees/$', views.add_employees, name='add_employees'),
    url(r'^manager/manage_employees/$', views.manage_employees, name='manage_employees'),

    # -------------- Employee section ------------------------ #

    url(r'^employee/$', views.emp_home, name='emp_home'),
]
