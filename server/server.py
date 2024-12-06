import os
from flask import Flask,request, jsonify, send_from_directory
import util
app = Flask(__name__)
util.load_saved_artifacts()

@app.route('/')
def index():
    client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../client')
    return send_from_directory(client_dir, 'app.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../client'), filename)
    
@app.route('/get_location_names', methods=['GET'])  # Default route
def get_location_names():
    try:
        response = jsonify({
            'locations': util.get_location_names()
            
        })
        response.headers.add('Access-Control-Allow-Origin', '*')  # Fixed CORS header
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    #util.load_saved_artifacts()
    try:
        # Ensure the request contains the required form fields
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Get the estimated price using the util function
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')  # Fixed CORS header
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == "__main__":
    print("Flask server is running...")
    app.run(debug=True)
