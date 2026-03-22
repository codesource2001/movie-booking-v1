from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TheatreViewSet

router = DefaultRouter()
router.register(r'', TheatreViewSet, basename='theatre')

urlpatterns = [
    path('', include(router.urls)),
]
