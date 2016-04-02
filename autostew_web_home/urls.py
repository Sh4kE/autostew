from django.conf.urls import url
from django.views.generic.base import TemplateView

from autostew_web_home.views import HomeView

urlpatterns = [
    url(r'^faq', TemplateView.as_view(template_name='autostew_web_home/faq.html'), name='faq'),
    url(r'^', HomeView.as_view(), name='home'),
]
