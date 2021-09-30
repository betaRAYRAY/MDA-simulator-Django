from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_input),
    path('results/', views.show_results),
    path('howto/', views.show_howto)
]