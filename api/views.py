from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
from django.http import HttpResponseBadRequest, HttpResponseServerError
from .utils import determinar_tipo_persona
from main.models import Contribuyente, EstadoContribuyente
from django.views.decorators.csrf import csrf_exempt
from .assistants.openai_client import *
from .assistants.utils import *
import os
#ASSISTANT_ID = os.getenv('ASSISTANT_ID_IA')

@csrf_exempt
def assistant_ai(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    # Obtener los datos del POST
    user_id = request.POST.get('user_id')
    user_content = request.POST.get('message')
    file_name = request.POST.get('archivo')

    if not user_id or not user_content:
        return JsonResponse({"error": "user_id and message are required"}, status=400)

    # Verificar si se debe olvidar la conversación
    if file_name == "forget":
        if user_id in user_conversations:
            del user_conversations[user_id]
            return JsonResponse({"response": "Conversación olvidada correctamente"})
        else:
            return JsonResponse({"response": "Correcto ya no recuerdo nada de ti"})

    # Manejar la subida de archivos
    file_id, file_path = handle_file_upload(file_name)
    
    if file_name and file_name != "" and not file_id:
        return JsonResponse({"error": "File not found or invalid file type"}, status=400)

    # Crear o recuperar un Thread para el usuario
    if user_id not in user_conversations:
        thread = client.beta.threads.create()
        user_conversations[user_id] = {"thread_id": thread.id}
        thread_id = thread.id
    else:
        thread_id = user_conversations[user_id]["thread_id"]

    # Adjuntar el archivo al mensaje si existe
    attachments = []
    if file_id:
        attachments.append({
            "file_id": file_id,
            "tools": [{"type": "file_search"}]
        })

    # Agregar el mensaje del usuario al Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_content,
        attachments=attachments if attachments else None
    )

    # Ejecutar el asistente en el Thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Esperar a que el asistente termine de procesar
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    # Obtener los mensajes del Thread
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # Obtener la respuesta del asistente
    assistant_response = messages.data[0].content[0].text.value

    # Eliminar el archivo si se subió
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return JsonResponse({"response": assistant_response})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    content = {'message': 'Esta vista está protegida por JWT'}
    return Response(content)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    data = {"message": "Esta es una vista protegida por token JWT."}
    return Response(data)




@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def consulta_ruc(request, ruc):
    if not ruc:
        return JsonResponse({'error': 'El parámetro RUC es requerido'}, status=400)

    if not ruc.isdigit() or len(ruc) != 11:
        return JsonResponse({'error': 'RUC debe tener exactamente 11 dígitos numéricos'}, status=400)

    try:
        empresa = Contribuyente.objects.select_related('estado_del_contribuyente').get(ruc=ruc)

        tipo_persona = determinar_tipo_persona(empresa.ruc)

        response = {
            'ruc': empresa.ruc,
            'nombre_o_razon_social': empresa.nombre_o_razon_social,
            'estado_contribuyente': empresa.estado_del_contribuyente.descripcion,
            'tipo_persona': tipo_persona
        }

        
        return JsonResponse(response)

    except Contribuyente.DoesNotExist:
        return JsonResponse({'error': 'RUC no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error en la base de datos: {str(e)}'}, status=500)



@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def consulta_dni(request, dni):
    if not dni:
        return JsonResponse({'error': 'El parámetro DNI es requerido'}, status=400)

    if not dni.isdigit() or len(dni) != 8:
        return JsonResponse({'error': 'DNI debe tener exactamente 8 dígitos numéricos'}, status=400)

    try:
        persona = Contribuyente.objects.select_related('estado_del_contribuyente').filter(ruc__startswith=f"10{dni}").first()

        if persona is None:
            return JsonResponse({'error': 'DNI no encontrado'}, status=404)

        tipo_persona = determinar_tipo_persona(persona.ruc)

        response = {
            'dni': dni,
            'ruc': persona.ruc,
            'nombre_completo': persona.nombre_o_razon_social,
            'estado_contribuyente': persona.estado_del_contribuyente.descripcion,
            'tipo_persona': tipo_persona
        }

        return JsonResponse(response)

    except Contribuyente.DoesNotExist:
        return JsonResponse({'error': 'DNI no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error en la base de datos: {str(e)}'}, status=500)