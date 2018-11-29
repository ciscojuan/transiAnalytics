from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crashesbyGender/', views.crashesbyGender, name='crashesbyGender'),
    path('crashesbymovilKind/', views.crashesbymovilKind, name='crashesbymovilKind'),
    path('crashesbyEscolaridad/', views.crashesByEscolaridad, name='crashesbyEscolaridad'),
    path('crashesbyEdad/', views.crashesbyEdad, name='crashesbyEdad'),
    path('crashesbyCivil', views.crashesbyCivil, name='crashesbyCivil'),

    path('diesbyGender/', views.diesbyGender, name='diesbyGender'),
    path('diesbymovilKind/', views.diesbymovilKind, name='diesbymovilKind'),
    path('diesbyEscolaridad/', views.diesByEscolaridad, name='diesbyEscolaridad'),
    path('diesbyEdad/', views.diesByEdad, name='diesbyEdad'),
    path('diesbyCivil/', views.diesbyCivil, name='diesbyCivil'),
]
