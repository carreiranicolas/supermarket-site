from django.urls import path
from . import views

app_name = "contas"

urlpatterns = [
    path('', views.home_contas, name='home_contas' ),
]
