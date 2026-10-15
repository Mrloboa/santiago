from flask import Flask, render_template, request, jsonify, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY', '1626')

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# --- RUTAS DE NAVEGACIÓN ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('SERVICIOS.html')

@app.route('/empresa')
def empresa():
    return render_template('EMPRESAS.html')

@app.route('/testimonios')
def testimonios():
    return render_template('TESTIMONIOS.html')

@app.route('/contacto')
def contacto():
    return render_template('CTA.html')

@app.route('/formulario')
def formulario():
    return render_template('form.html')

# --- RUTA DE LÓGICA (Envío de correo) ---
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje = request.form.get('mensaje')

        if not nombre or not correo or not mensaje:
            return jsonify({'status': 'error', 'message': 'Todos los campos son obligatorios.'}), 400

        msg = Message(
            'Nuevo lead desde tu Portafolio',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}"

        mail.send(msg)
        return jsonify({'status': 'success', 'message': '¡Mensaje enviado correctamente! Me pondré en contacto contigo pronto.'}), 200

    except Exception as e:
        print(f"Error enviando correo: {e}")
        return jsonify({'status': 'error', 'message': 'Ocurrió un error en el servidor. Intenta de nuevo más tarde.'}), 500

# --- CABECERAS DE SEGURIDAD ---
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == "__main__":
    app.run(debug=True)