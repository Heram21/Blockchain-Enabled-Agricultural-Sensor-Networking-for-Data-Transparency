import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import serial

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Soil Moisture Sensor
MOISTURE_PIN = 17  # GPIO17 (Pin 11)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

# DHT11 Sensor
DHT_PIN = board.D4  # GPIO4 (Pin 7)
dht_device = adafruit_dht.DHT11(DHT_PIN)

# pH Sensor (UART Communication)
ser = serial.Serial(
    port='/dev/serial0',  # UART port on Raspberry Pi
    baudrate=9600,        # Check your sensor's datasheet for the correct baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Function to read soil moisture
def read_soil_moisture():
    moisture_state = GPIO.input(MOISTURE_PIN)
    return "Dry" if moisture_state == GPIO.HIGH else "Moist"

# Function to read DHT11 sensor
def read_dht11():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return humidity, temperature
    except RuntimeError as e:
        print(f"DHT11 Error: {e}")
        return None, None

# Function to read pH sensor
def read_ph():
    ser.write(b'R\r\n')  # Send command to request pH data
    time.sleep(1)        # Wait for the sensor to respond
    raw_response = ser.readline().decode('utf-8', errors='ignore').strip()
    ph_value = None
    if "PH:" in raw_response:
        try:
            ph_start = raw_response.index("PH:") + 3
            ph_end = raw_response.index(",", ph_start)
            ph_value = float(raw_response[ph_start:ph_end])
        except Exception as e:
            print(f"Error parsing pH value: {e}")
    return ph_value

# Function to log data to a file
def log_data(data):
    with open("sensor_data.txt", "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}: {data}\n")

# Main loop
try:
    while True:
        # Read data from all sensors
        soil_moisture = read_soil_moisture()
        humidity, temperature = read_dht11()
        ph_value = read_ph()

        # Handle missing or invalid readings
        humidity = humidity if humidity is not None else "N/A"
        temperature = temperature if temperature is not None else "N/A"
        ph_value = ph_value if ph_value is not None else "N/A"

        # Combine data into a dictionary
        sensor_data = {
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "ph_value": ph_value
        }

        # Log data locally
        log_data(sensor_data)

        # Print data to the console
        print(f"Soil Moisture: {sensor_data['soil_moisture']}")
        print(f"Temperature: {sensor_data['temperature']}Â°C")
        print(f"Humidity: {sensor_data['humidity']}%")
        print(f"pH Value: {sensor_data['ph_value']}")
        print("-" * 30)

        # Wait before the next reading
        time.sleep(60)  # Wait 60 seconds

except KeyboardInterrupt:
    print("Script stopped.")
    GPIO.cleanup()
