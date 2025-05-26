from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import protected_view
from .views import consulta_ruc, consulta_dni
from .views import assistant_ai

#todas estas rutas requieren el prefijo /api 
urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', protected_view, name='protected_view'),
    path('ruc/<str:ruc>', consulta_ruc, name='consulta_ruc'),
    path('dni/<str:dni>', consulta_dni, name='consulta_dni'),
    path('assistant_ai/', assistant_ai, name='assistant_ai'),
]