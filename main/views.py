from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Modelo de usuario de Django
from django.shortcuts import render, redirect
from django.conf import settings
import json, requests
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

@login_required(login_url='/admin/login/')  # Redirige si no está autenticado
def create_token(request):
    # El usuario está garantizado que está autenticado gracias a @login_required
    user = request.user
    
    # Recibir variables del request (GET, POST o JSON)
    # Podemos seguir recibiendo parámetros adicionales si es necesario
    parametro_extra = request.GET.get('parametro', 'valor_por_defecto')
    
    # Variables para enviar al template con los datos del usuario
    contexto = {
        'titulo': 'Mi Página Personalizada',
        'usuario': user.username,
        'email': user.email,
        'nombre_completo': user.get_full_name(),  # Si tienes first_name y last_name
        'fecha_registro': user.date_joined,  # Fecha de registro del usuario
        'es_staff': user.is_staff,  # Si es parte del staff/admin
        'parametro_extra': parametro_extra,
        # Puedes agregar más datos del usuario según necesites
    }
    
    return render(request, 'main/jwt_credentials/create_token.html', contexto)

@login_required(login_url='/admin/login/')
def get_token_main(request):
    contexto = {
        'titulo': 'Token',
        'usuario': request.user.username,
        'email': request.user.email,
        'exito': False,
        'token_data': None
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                # Configurar la URL del endpoint de tokens
                token_url = f"{settings.BASE_URL}/api/token/" if hasattr(settings, 'BASE_URL') else 'http://127.0.0.1:8000/api/token/'
                
                # Hacer la petición POST al endpoint JWT
                response = requests.post(
                    token_url,
                    data={
                        'username': username,
                        'password': password
                    }
                )

                if response.status_code == 200:
                    token_data = response.json()
                    contexto.update({
                        'exito': True,
                        'token_data': token_data
                    })
                else:
                    contexto['error'] = "Credenciales inválidas"

            except requests.exceptions.RequestException as e:
                contexto['error'] = f"Error al conectar con el servidor: {str(e)}"
            except json.JSONDecodeError:
                contexto['error'] = "Respuesta inválida del servidor"

    return render(request, 'main/jwt_credentials/your_token.html', contexto)