from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/server2')
def server2_endpoint():
    return jsonify({
        'message': 'Hello from Server2!'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
