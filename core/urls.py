from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import CustomTokenObtainPairView

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
