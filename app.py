
from flask import Flask,jsonify, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_list = [5,6,13,16,19,20,21,26]
gpio_dict = {5:False, 6:False, 13:False, 16:False, 19:False, 20:False, 21:False, 26:False}

for i in gpio_list:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

@app.route('/')
def home():
    return render_template('index.html', gpio_list=gpio_list)

@app.route('/gpio_control', methods=['GET', 'POST'])
def gpio_control():
    if request.method == 'POST':
        # Get the form data
        pin = request.form['pin']
        state = request.form['state']
        # Do something with the form data, like control the GPIO pins
        # ...
        # Render the template with the updated GPIO list
        return render_template('index.html', gpio_list=gpio_list)
    else:
        # Render the template with the initial GPIO list
        return render_template('index.html', gpio_list=gpio_list)

@app.route("/gpio/<int:pin>", methods=["POST"])
def toggle_pin(pin):
    state = request.json["state"]
    if state == "On":
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    return jsonify({"success": True})

@app.route('/on/<int:gpio>')
def gpio_on(gpio):
    if gpio in gpio_list:
        GPIO.output(gpio, GPIO.LOW)
        return jsonify({'message': f'GPIO is now ON for pin {gpio}'})
    else:
        return jsonify({'message': f'GPIO pin {gpio} is not available.'})

@app.route('/off/<int:gpio>')
def gpio_off(gpio):
    if gpio in gpio_list:
        GPIO.output(gpio, GPIO.HIGH)
        return jsonify({'message': f'GPIO is now OFF for pin {gpio}'})
    else:
        return jsonify({'message': f'GPIO pin {gpio} is not available.'})
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
