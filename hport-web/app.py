from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'hport-web'})

@app.route('/api/data')
def get_data():
    return jsonify({
        'message': 'Hello from hport web app!',
        'data': []
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
