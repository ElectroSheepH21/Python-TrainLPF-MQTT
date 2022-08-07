import RPi.GPIO as GPIO
import configparser
import paho.mqtt.client as mqtt

from motorlpf import MotorLPF

in1_pin = 14
in2_pin = 15
pwm_pin = 18
standby_pin = 23

GPIO.setwarnings(False)
motor_lpf = MotorLPF(in1_pin, in2_pin, pwm_pin, standby_pin)
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        mqtt_client.subscribe('/train/speed')
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg):
    if msg.topic == '/train/speed':
        speed_percentage = float(msg.payload.decode('utf-8'))
        speed = int(speed_percentage)
        print(f"Speed: {speed}%")
        motor_lpf.update_speed(speed)


if __name__ == '__main__':
    try:
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        with open('/home/pi/Python-TrainLPF-MQTT/config.ini', 'r') as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
            mqtt_client.username_pw_set(config['broker']['username'], config['broker']['password'])
            mqtt_client.connect(config['broker']['host'], int(config['broker']['port']))
            mqtt_client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
