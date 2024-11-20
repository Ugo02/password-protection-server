from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/server1')
def server1_endpoint():
    # Fetch data from server2
    try:
        response = requests.get('http://server2:5001/api/server2')
        data = response.json()
    except Exception as e:
        data = {'error': str(e)}

    return jsonify({
        'message': 'Hello from Server1!',
        'data_from_server2': data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
