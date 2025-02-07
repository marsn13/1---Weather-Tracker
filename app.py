from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Insira aqui sua chave de API do OpenWeatherMap
API_KEY = '7f5487eec6d7b953fd3d8b6afdd42b5c'
# Parâmetros padrão: unidades métricas (°C) e idioma inglês (ou 'pt' para português)
UNITS = 'metric'
LANG = 'en'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'O parâmetro "city" é obrigatório.'}), 400

    # Constrói a URL da API do OpenWeatherMap
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}&lang={LANG}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Não foi possível obter os dados meteorológicos.'}), response.status_code
    
    data = response.json()
    # Extrai as informações relevantes
    weather_info = {
        'city': data.get('name'),
        'temperature': data.get('main', {}).get('temp'),
        'humidity': data.get('main', {}).get('humidity'),
        'description': data.get('weather')[0].get('description') if data.get('weather') else 'N/A'
    }
    
    return jsonify(weather_info)

if __name__ == '__main__':
    # Ative debug=True para desenvolvimento
    app.run(debug=True)
