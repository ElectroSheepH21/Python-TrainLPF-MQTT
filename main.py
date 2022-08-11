import json
import time

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from motor_lpf import MotorLPF
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
from pathlib import Path

in1_pin = 14
in2_pin = 15
pwm_pin = 18
standby_pin = 23
mqtt_topics = []

GPIO.setwarnings(False)
motor_lpf = MotorLPF(in1_pin, in2_pin, pwm_pin, standby_pin)
mqtt_client = mqtt.Client()
try:
    display = get_device()
except:
    display = None
    print("Display not found --> Display not available")

try:
    font_path = str(Path(__file__).parent.resolve().joinpath('C&C Red Alert [INET].ttf'))
    font = ImageFont.truetype(font_path, 12)
except IOError:
    display = None
    print("Font file not found --> Display not available")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        for topic in mqtt_topics:
            mqtt_client.subscribe(topic['path'], int(topic['qos']))
            mqtt_client.publish(topic['path'], topic['initialValue'])
    else:
        print(f"Error[{rc}], check config.json")


def on_message(client, userdata, msg):
    if msg.topic == '/train/speed':
        speed_percentage = float(msg.payload.decode('utf-8'))
        speed = int(speed_percentage)
        print(f"Speed: {speed}%")
        motor_lpf.update_speed(speed)
    elif msg.topic == '/train/display_text' and display is not None:
        text = msg.payload.decode('utf-8')
        print(f"Display text: {text}")
        with canvas(display) as draw:
            text = msg.payload.decode('utf-8')
            text_position = (display.width / 2 - font.getsize(text)[0] / 2, display.height / 2 - font.getsize(text)[1] / 2)
            draw.text(text_position, text, font=font, fill="white")
            time.sleep(0.1)  # Wait for the display to update


if __name__ == '__main__':
    try:
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        try:
            config_path = str(Path(__file__).parent.resolve().joinpath('config.json'))
            with open(config_path, 'r') as f:
                config = json.loads(f.read())
                mqtt_topics = config['mqtt']['topics']
                mqtt_client.username_pw_set(config['mqtt']['username'], config['mqtt']['password'])
                try:
                    mqtt_client.connect(config['broker']['host'], int(config['broker']['port']))
                    mqtt_client.loop_forever()
                except:
                    print("Broker not available, check config.json")
        except IOError:
            print("Config file not found")
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
