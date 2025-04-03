from flask import Flask, request, jsonify, send_from_directory
from googlesearch import search
import time
import urllib.parse

app = Flask(__name__)

def is_same_canonical(url1, url2):
    """
    Сравнивает канонические части двух URL, игнорируя параметры и завершающий слэш.
    """
    p1 = urllib.parse.urlparse(url1)
    p2 = urllib.parse.urlparse(url2)
    return (p1.netloc.lower() == p2.netloc.lower()) and (p1.path.rstrip('/').lower() == p2.path.rstrip('/').lower())

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
    
    time.sleep(2.0)
    try:
        results = list(search(query, num_results=10))
    except Exception as e:
        return jsonify({'result': f'Ошибка при выполнении поиска: {str(e)}'})
    
    found = False
    for result in results:
        if is_same_canonical(url, result):
            found = True
            break
    
    if found:
        return jsonify({'result': 'Страница проиндексирована'})
    else:
        return jsonify({'result': 'Страница НЕ проиндексирована'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
