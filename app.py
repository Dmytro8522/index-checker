from flask import Flask, request, jsonify, send_from_directory
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import time

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        time.sleep(1.5)
        response = requests.get(f"https://www.google.com/search?q={quote(query)}", headers=headers, timeout=10)

        if response.status_code != 200:
            return jsonify({'result': f'Google вернул код {response.status_code}'})

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('a') if 'href' in a.attrs]

        if any(url in link for link in links):
            return jsonify({'result': 'Страница проиндексирована'})
        else:
            return jsonify({'result': 'Страница НЕ проиндексирована'})
    except Exception as e:
        return jsonify({'result': f'Ошибка: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)