from flask import Flask, request, render_template, jsonify
import sett
import os
import services
import datetime
import time
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = sett.UPLOAD_FOLDER

@app.route("/")
def index():
	return render_template("index.html", now=datetime.datetime.now() , algo="algo más")

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo mundoso de nuevo'

@app.route('/pdf_comprobante', methods=['POST'])
def pdf_comprobante():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró el archivo'}), 400
    
    file = request.files['file']
    telefono = request.form.get('telefono')
    
    if file.filename == '' or not sett.allowed_file(file.filename):
        return jsonify({'error': 'Archivo no válido'}), 400
    
    if not telefono:
        return jsonify({'error': 'Número de teléfono no proporcionado'}), 400
    
    # Crear la carpeta temporal si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    try:
        # Guardar el archivo
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Crear el body para el envio del documento       
        #headers, data, files = services.document_FromLocalFile_Message(telefono, file_path, filename)
        
        # Primero, cargamos el documento
        media_id = services.upload_document(file_path)
        
        # Luego, enviamos el mensaje con el ID del medio
        whatsapp_response = services.send_pdf_whatsapp(telefono, media_id, filename)
                            
         # Cerrar todos los manejadores de archivo
        file.close()
        
        # Intentar eliminar el archivo
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                os.remove(file_path)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(1)  # Esperar 1 segundo antes de intentar de nuevo
                else:
                    print(f"No se pudo eliminar el archivo {file_path} después de {max_attempts} intentos")
        
        return jsonify({
            'message': 'PDF recibido y enviado por WhatsApp',
            'whatsapp_response': whatsapp_response
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge is not None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return str(e), 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        message_id = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        
        services.administrar_chatbot(text, number, message_id, name)
        return 'enviado correctamente'
        
    except Exception as e:
        return 'no enviado' + str(e)

if __name__ == '__main__':
    app.run(debug=True)