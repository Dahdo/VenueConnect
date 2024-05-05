from django.urls import path
from venues import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'venues', views.VenueViewset, basename='venues')

urlpatterns = [
    path('', include(router.urls)),
]