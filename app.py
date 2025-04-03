from flask import Flask, request, jsonify, send_from_directory
from googlesearch import search
import time
import urllib.parse

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
    
    query = f"site:{urllib.parse.quote(url)}"
    canonical_url = url.rstrip('/')
    
    time.sleep(2.0)
    try:
        results = list(search(query, num_results=10))
    except Exception as e:
        return jsonify({'result': f'Ошибка при выполнении поиска: {str(e)}'})
    
    found = False
    for result in results:
        if urllib.parse.urlparse(result).netloc + urllib.parse.urlparse(result).path == urllib.parse.urlparse(canonical_url).netloc + urllib.parse.urlparse(canonical_url).path:
            found = True
            break
    
    if found:
        return jsonify({'result': 'Страница проиндексирована'})
    else:
        return jsonify({'result': 'Страница НЕ проиндексирована'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
