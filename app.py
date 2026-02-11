from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Récupère l'IP du visiteur sur Render
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    # Géolocalisation par IP (au cas où il refuse le GPS)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        ip_lat = response.get('lat', 48.8566)
        ip_lon = response.get('lon', 2.3522)
        city = response.get('city', 'Inconnue')
    except:
        ip_lat, ip_lon, city = 48.8566, 2.3522, "Paris"

    return render_template('index.html', ip_lat=ip_lat, ip_lon=ip_lon, city=city)

if __name__ == '__main__':
    app.run()