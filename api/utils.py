# api/utils.py

def determinar_tipo_persona(ruc):
    if not ruc or len(ruc) < 2:
        return "DESCONOCIDO"
    
    primeros_digitos = ruc[:2]
    
    if primeros_digitos == "10":
        return "PERSONA NATURAL"
    elif primeros_digitos == "20":
        return "PERSONA JURÍDICA"
    elif primeros_digitos == "15":
        return "PERSONA NATURAL EXTRANJERA"
    elif primeros_digitos == "16":
        return "PERSONA JURÍDICA EXTRANJERA"
    elif primeros_digitos == "17":
        return "EMBAJADAS Y ORGANISMOS INTERNACIONALES"
    else:
        return "OTRO TIPO"