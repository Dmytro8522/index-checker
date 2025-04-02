from flask import Flask, request, jsonify, send_from_directory
import requests
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/check', methods=['POST'])
def check_index():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'result': 'URL не указан'})

    query = f"site:{url}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(f"https://www.google.com/search?q={quote(query)}", headers=headers)

    if response.status_code != 200:
        return jsonify({'result': 'Ошибка запроса к Google'})

    if url in response.text:
        return jsonify({'result': 'Страница проиндексирована'})
    else:
        return jsonify({'result': 'Страница НЕ проиндексирована'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)