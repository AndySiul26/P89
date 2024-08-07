import requests
import sett
import json, os
import time

# Para establecer las librerías necesarias 
# usamos el comando pip freeze > requirements.txt

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def upload_document(file_path):
    whatsapp_token = sett.whats_app_token
    whatsapp_url = sett.whatsapp_url
    
    
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'file': file
        }
        data = {
            'messaging_product': 'whatsapp',         
        }
        
        response = requests.post(whatsapp_url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        return response.json().get('id')
    else:
        raise Exception(f"Error al cargar el documento: {response.text}")

def send_pdf_whatsapp(telefono, media_id, filename):
    whatsapp_token = sett.whats_app_token
    whatsapp_url = sett.whatsapp_url
    
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': telefono,
        'type': 'document',
        'document': {
            'id': media_id,
            'caption': 'Tu comprobante',
            'filename': filename
        }
    }
    
    response = requests.post(whatsapp_url, headers=headers, json=data)
    return response.json()

def enviar_Mensaje_Whatsapp(data, files=None, headers=None):
    try:
        whatsapp_token = sett.whats_app_token
        whatsapp_url = sett.whatsapp_url
        if headers == None:
            headers = {        
                'Authorization': 'Bearer ' + whatsapp_token,
                'Content-Type': 'application/json'
                }
        
        print("Inicio de respuesta")
        if files is not None:
            print(headers)
            print(data)
            print(files)
        
        response = requests.post(whatsapp_url, headers=headers, json=data, files=files)
        if response.status_code == 200:
            print (response.text)
            return 'mensaje enviado', 200
        else:                
            print(response.text)     
            print ("Datos: ", data)
            return 'no se pudo enviar el mensaje', response.status_code
    except Exception as e:
        print(str(e))
        return str(e), 403
    
def text_Message(number, text):
    try:
        test = 1
        if test == 1:
            data = {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "preview_url": "false",
                    "body": text
                }
            }
        elif test == 2:
            data = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "template",
                "template": {
                    "name": "bienvenida",
                    "language": {
                    "code": "ES"
                    }
                }
            }
        
        
    except Exception as e:
        print("error en text_Message: ", e)    
        
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data =  {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    
    return data

def document_Message(number, url, caption, filename):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    
    return data

def document_FromLocalFile_Message(number, file_path, caption):
   
    headers = {
        "Authorization": f"Bearer {sett.whats_app_token}",
    }
   
    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': number,
        'type': 'document',
    }
    
    files = {
        'file': (caption, open(file_path, 'rb'), 'application/pdf')
    }
    
    return headers, data, files
    

def sticker_Message(number, sticker_id):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    
    return data

def replyText_Message(number, messageId, text):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    
    return data

def markRead_Message(messageId):
    data =  {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    
    return data


def administrar_chatbot(text, number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        body = "¡Hola! 👋 Bienvenido a Portal 89. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo Portal 89"
        options = ["✅ servicios", "📅 agendar cita"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?"
        footer = "Equipo Bigdateros"
        options = ["Analítica Avanzada", "Migración Cloud", "Inteligencia de Negocio"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        # sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        # list.append(sticker)
    elif "inteligencia de negocio" in text:
        body = "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con una introducción a nuestros métodos de Inteligencia de Negocio?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, envía el PDF.", "⛔ No, gracias"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "sí, envía el pdf" in text:
        # sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento.")

        # enviar_Mensaje_Whatsapp(sticker)
        enviar_Mensaje_Whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Listo 👍🏻", "Inteligencia de Negocio.pdf")
        enviar_Mensaje_Whatsapp(document)
        time.sleep(3)

        body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, agenda reunión", "No, gracias." ]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "sí, agenda reunión" in text :
        body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
        footer = "Equipo Portal 89"
        options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]

        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "7 de junio, 2:00 pm" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        footer = "Equipo Portal 89"
        options = ["✅ Sí, por favor", "❌ No, gracias."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "no, gracias." in text:
        textMessage = text_Message(number, "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
    else:
        data = text_Message(number,"Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    data = ''
    for item in list:
        data += ' ' + str( enviar_Mensaje_Whatsapp(item))