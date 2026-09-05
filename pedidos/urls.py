from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('', views.home_pedidos, name='home_pedidos' ),
]
