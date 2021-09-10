from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('api/data/', views.get_delete),
    path('api/data/add/', views.add),
    path('api/data/list/', views.show)
]
