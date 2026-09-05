from django.urls import path
from . import views

app_name = "carrinhos"

urlpatterns = [
    path('', views.home_carrinho, name='home_carrinho' ),
]
