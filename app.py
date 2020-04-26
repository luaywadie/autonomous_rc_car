from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO          
import time
import dht11 # Github Adafruit Therm and Humidity Sensor Parser
import threading

app = Flask(__name__)

current_position = 22
target_position = 0
condition = False
data = [
    {'type' : 0},
    {'type' : 0},
    {'type' : 4},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 0},
    {'type' : 1},
    {'type' : 0},
    {'type' : 0},
]

def startSurv():
    global current_position, target_position, condition, data
    # Check if there
    if (current_position == target_position):
        condition = True
        return

    if (current_position > target_position):
        if (movePossible("n")):
            data[current_position]['type'] = 0
            data[current_position - 5]['type'] = 1
            current_position -= 5
            
    threading.Timer(5.0,startSurv).start()
        
# RC

# Core Variables
area = [1,2]
temp = 0
hum = 0

# Variables
in1 = 27
in2 = 22
in3 = 17
in4 = 18
en1 = 24
en2 = 26

TRIG = 6
ECHO = 5

B_LED = 16
Y_LED = 25

GPIO.setmode(GPIO.BCM)
# Motors
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.setup(B_LED,GPIO.OUT)
GPIO.setup(Y_LED,GPIO.OUT)

p1 = GPIO.PWM(en1,1000)
p2 = GPIO.PWM(en2,1000)
p1.start(0)
p2.start(0)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Functions Sensors
# Ultrasonic
def getDistance():
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)

	while GPIO.input(ECHO) == False:
		pass
	start = time.time()

	while GPIO.input(ECHO) == True:
		pass
	end = time.time()
	
	if ((end - start) * 17000 < 25):
		GPIO.output(Y_LED,GPIO.HIGH)
	else:
		GPIO.output(Y_LED,GPIO.LOW)

	return (end - start) * 17000

def getTemp():
	# read data using Pin GPIO21 
	instance = dht11.DHT11(pin=23)

	while True:
		result = instance.read()
		if result.is_valid():
			# print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
			return result

# New


def movePossible(dir):
    global current_position, data
    if (dir == "n"):
        if (current_position - 5 >= 0):
            # Read distance sensor and check if object infront exists
            distance = getDistance()
            if (distance > 30):
                data[current_position - 5]['type'] = 1
                data[current_position]['type'] = 5
                current_position -= 5
                return True
            else:
                data[current_position - 5]['type'] = 3
                return False
        return False
    elif (dir == "w"):
        if (current_position not in [0,5,10,15,20]):
            moveLeftNow()
            time.sleep(1)
            # Read distance sensor and check if object infront exists
            distance = getDistance()
            if (distance > 30):
                data[current_position - 1]['type'] = 1
                data[current_position]['type'] = 5
                current_position = current_position - 1

                moveForwardNow()
                time.sleep(.5)
                return True
            else:
                moveRightNow()
                data[current_position - 1]['type'] = 3
                return False
        return False
    elif (dir == "e"):
        if (current_position not in [4,9,14,19,24]):
            moveRightNow()
            time.sleep(1)
            distance = getDistance()
            if (distance > 30):
                data[current_position + 1]['type'] = 1
                data[current_position]['type'] = 5
                current_position += 1
                moveForwardNow()
                time.sleep(.5)
                return True
            else:
                moveLeftNow()
                data[current_position + 1]['type'] = 3
                return False
        return False
    elif (dir == "s"):
        if (current_position + 5 <= 24):
            moveLeftNow()
            time.sleep(.5)
            moveLeftNow()
            time.sleep(.5)
            distance = getDistance()
            if (distance > 30):
                data[current_position + 5]['type'] = 1
                data[current_position]['type'] = 5
                current_position += 5
                return True
            else:
                moveRightNow()
                time.sleep(.5)
                moveRightNow()
                time.sleep(.5)
                return False
    return False

def setSectorObj(dir):
    global data, current_position
    if (dir == "n"):
        data[current_position - 5] = 3
    elif (dir == "w"):
        data[current_position - 1] = 3
    elif (dir == "e"):
        data[current_position + 1] = 3
    elif (dir == "s"):
        data[current_position + 5] = 3


# Functions Mobility
def resetGPIO():
	GPIO.output(in1,False)
	GPIO.output(in2,False)
	GPIO.output(in3,False)
	GPIO.output(in4,False)
	
def moveForwardNow():
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)
    GPIO.output(in1,True)
    GPIO.output(in2,False)
    GPIO.output(in3,True)
    GPIO.output(in4,False)
    time.sleep(.4)
    resetGPIO()
    
def moveForward():
    if (movePossible("n")):
        p1.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)
        GPIO.output(in1,True)
        GPIO.output(in2,False)
        GPIO.output(in3,True)
        GPIO.output(in4,False)
        time.sleep(.4)
        resetGPIO()
    else:
        print("Can't move")

def moveBackward():
    if (movePossible("s")):
        moveForwardNow()
        time.sleep(0.5)
        moveRightNow()
        time.sleep(.5)
        moveRightNow()
        time.sleep(.5)
    else:
        print("Can't move")
    
def moveLeftNow():
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)
    GPIO.output(in1,False)
    GPIO.output(in2,True)
    GPIO.output(in3,True)
    GPIO.output(in4,False)
    time.sleep(.4)
    resetGPIO()

def moveLeft():
    if (movePossible("w")):
        moveRightNow()
    else:
        print("Can't move")
    
def moveRightNow():
    print("Moving Right")
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)
    GPIO.output(in1,True)
    GPIO.output(in2,False)
    GPIO.output(in3,False)
    GPIO.output(in4,True)
    time.sleep(.4)
    resetGPIO()    

def moveRight():
    if (movePossible("e")):
        moveLeftNow()
    else:
        print("Can't move")
    
def cleanGPIO():
	GPIO.cleanup()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/start", methods=['GET','POST'])
def start():
    c = "ok"
    print("Here")
    return jsonify(r=c)
    
@app.route("/forward", methods=['POST'])
def forward():
    moveForward()
    return ""
    
@app.route("/backward", methods=['POST'])
def backward():
    moveBackward()
    return ""
    
@app.route("/left", methods=['POST'])
def left():
    moveLeft()
    return ""
    
@app.route("/right", methods=['POST'])
def right():
    moveRight()
    return ""

@app.route("/update", methods=['GET','POST'])
def update():
    global data, condition
    # if (condition):
    #     return jsonify(data="Done!")
    # else:
    return jsonify(data=data)

@app.route('/get_data', methods=['GET','POST'])
def get_data():
    result = getTemp()
    return jsonify(temp=[result.temperature],humidity=[result.humidity])

@app.route('/b_led', methods=['GET','POST'])
def b_led():
    if (GPIO.input(B_LED)):
        GPIO.output(B_LED, GPIO.LOW)
    else:
        GPIO.output(B_LED, GPIO.HIGH)
    return ""

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
