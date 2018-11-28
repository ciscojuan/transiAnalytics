from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crashesbyGender/', views.crashesbyGender, name='crashesbyGender'),
    path('diesbyGender/', views.diesbyGender, name='diesbyGender'),
    path('crashesbymovilKind/', views.crashesbymovilKind, name='crashesbymovilKind'),
    path('diesbymovilKind/', views.diesbymovilKind, name='diesbymovilKind'),
    path('diesbyEscolaridad/', views.diesByEscolaridad, name='diesbyEscolaridad'),
    path('reporte_homicidios/', views.reporte_homicidios, name='reporte_homicidios'),
]