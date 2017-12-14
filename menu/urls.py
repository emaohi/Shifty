from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^test/$', TemplateView.as_view(template_name='employee/menu/index.html'), name='menu_test'),
    ]
