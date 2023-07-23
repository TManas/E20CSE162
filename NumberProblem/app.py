from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    if not urls:
        return jsonify({'error': 'No URLs provided.'}), 400

    result = {}

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'numbers' in data and isinstance(data['numbers'], list):
                    result[url] = data['numbers']
                else:
                    result[url] = 'Invalid response format. Missing or invalid "numbers" field.'
            else:
                result[url] = f'Request to {url} failed with status code {response.status_code}.'
        except Exception as e:
            result[url] = f'Error retrieving data from {url}: {str(e)}'

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
