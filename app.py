from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Récupération de l'IP réelle du visiteur
    # On vérifie X-Forwarded-For pour Render/Ngrok, sinon on prend l'IP standard
    ip_raw = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_address = ip_raw.split(',')[0].strip()

    # Nettoyage pour le local (si l'IP est ::1 ou 127.0.0.1, on affiche une IP fictive pour le style)
    display_ip = ip_address
    if ip_address in ['127.0.0.1', '::1']:
        display_ip = "192.168.1.42 (Local)"

    # 2. Géolocalisation par IP (Base de repli si le pote refuse le GPS)
    try:
        # On utilise une API gratuite pour trouver la ville via l'IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}?lang=fr").json()
        if response.get('status') == 'success':
            city = response.get('city', 'Inconnue')
            ip_lat = response.get('lat', 48.8566)
            ip_lon = response.get('lon', 2.3522)
        else:
            city, ip_lat, ip_lon = "Localisation masquée", 48.8566, 2.3522
    except:
        city, ip_lat, ip_lon = "Serveur indisponible", 48.8566, 2.3522

    # 3. Envoi des données au template HTML
    return render_template('index.html', 
                           ip_address=display_ip, 
                           city=city, 
                           ip_lat=ip_lat, 
                           ip_lon=ip_lon)

if __name__ == '__main__':
    # host='0.0.0.0' est nécessaire pour être accessible sur le réseau local
    # port=5000 est le standard pour Flask
    app.run(host='0.0.0.0', port=5000, debug=True)