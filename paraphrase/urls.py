from django.urls import path
from . import views

urlpatterns = [
    path('paraphrase', views.paraphrase, name='paraphrase'),
]