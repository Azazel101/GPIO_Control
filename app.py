
from flask import Flask,jsonify, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_dict = {5:False, 6:False, 13:False, 16:False, 19:False, 20:False, 21:False, 26:False}

for i in gpio_dict:
    GPIO.setup(i, GPIO.OUT)
    if gpio_dict[i] == False:
        GPIO.output(i, GPIO.HIGH)
    else:
        GPIO.output(i, GPIO.LOW)


@app.route('/')
def home():
    print(gpio_dict)
    return render_template('index.html', gpio_list=gpio_dict)

@app.route("/gpio/<int:pin>", methods=["POST"])
def toggle_pin(pin):
    state = request.json["state"]
    if state == "On":
        GPIO.output(pin, GPIO.HIGH)
        gpio_dict[pin] = True  
    else:
        GPIO.output(pin, GPIO.LOW)
        gpio_dict[pin] = False 
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
