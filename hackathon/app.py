from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

# Path to the sensor data file
DATA_FILE = "sensor_data.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_sensor_data():
    # Read the sensor data from the file
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "Data file not found"}), 404

    with open(DATA_FILE, "r") as f:
        lines = f.readlines()

    # Parse the data into a list of dictionaries
    sensor_data = []
    for line in lines:
        try:
            timestamp, data_str = line.strip().split(": ", 1)
            data_dict = eval(data_str)  # Convert string representation of dict to actual dict
            data_dict["timestamp"] = timestamp
            sensor_data.append(data_dict)
        except Exception as e:
            print(f"Error parsing line: {line}, Error: {e}")

    # Return the data as JSON
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
