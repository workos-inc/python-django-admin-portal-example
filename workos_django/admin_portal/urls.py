from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('provision_enterprise/', views.provision_enterprise, name='provision_enterprise'),
    path('admin_portal/', views.admin_portal, name='admin_portal')
]