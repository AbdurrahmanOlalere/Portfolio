#bsic flask api setup for forum api and other api calls in the future, not currently used but will be in the future for contact form and forum
from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, this is your data!'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='localhost', port='5001', debug=True)