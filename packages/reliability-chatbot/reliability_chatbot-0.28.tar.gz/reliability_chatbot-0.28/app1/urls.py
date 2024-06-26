from django.urls import path
from .views import ValidateAPIView

urlpatterns = [
    path('api/validate-key/', ValidateAPIView.as_view(), name='validate-api-key'),
]
