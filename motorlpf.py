import RPi.GPIO as GPIO


class MotorLPF:
    def __init__(self, in1_pin, in2_pin, pwm_pin, standby_pin, reverse=False):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.pwm_pin = pwm_pin
        self.standby_pin = standby_pin
        self.reverse = reverse

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1_pin, GPIO.OUT)
        GPIO.setup(in2_pin, GPIO.OUT)
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(standby_pin, GPIO.OUT)

        GPIO.output(standby_pin, GPIO.HIGH)
        self.pwm = GPIO.PWM(pwm_pin, 1000)
        self.pwm.start(0)

    def update_speed(self, speed):
        duty_cycle = speed

        if speed < 0:
            duty_cycle *= -1

        if self.reverse:
            speed *= -1

        if speed > 0:
            self.drive_forwards()
        elif speed < 0:
            self.drive_backwards()
        else:
            self.brake()

        self.pwm.ChangeDutyCycle(duty_cycle)

    def drive_forwards(self):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def drive_backwards(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def brake(self):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def standby(self, value):
        self.brake()
        GPIO.output(self.standby_pin, not value)
