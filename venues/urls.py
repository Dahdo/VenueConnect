from django.urls import path
from venues import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'venues', views.VenueViewset, basename='overview')
router.register(r'venue-filter', views.VenueSearchFilter, basename='venue-filter')

urlpatterns = [
    path('', include(router.urls)),
]