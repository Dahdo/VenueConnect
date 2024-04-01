from django.urls import path
from users import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'registration', views.RegistrationViewSet, basename='registration')
router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'logout', views.LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]

