import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file_name):
    file_id = None
    file_path = None
    
    if file_name and file_name != "":
        base_path = "/var/www/html/"+os.getenv("PROJECT_PATH")+"/asistente_lyon/"
        file_path = os.path.join(base_path, file_name)
        
        if os.path.exists(file_path) and allowed_file(file_name):
            with open(file_path, "rb") as f:
                file_response = client.files.create(
                    file=f,
                    purpose="assistants"
                )
            file_id = file_response.id
    
    return file_id, file_path