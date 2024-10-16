from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('category_filter/<str:category_name>/', views.category_filter, name='category_filter'),
] 