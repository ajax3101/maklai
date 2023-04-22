from django.urls import path
from . import views


urlpatterns = [
    path('', views.paraphrase_view, name='paraphrase'),
    path('index', views.index, name='home'),
]