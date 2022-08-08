# Python-TrainLPF-MQTT

## Overview
This repository provides a Python script which allows to control a Lego Power Functions (LPF) train via the MQTT protocol. For the interaction with the LPF motor the TB6612FNG H-bridge driver IC was used. This IC provides a low voltage drop and fits due to its size well into the train. This project was created with a Raspberry Pi Zero and the Raspberry Pi OS on it. Therefore the username in the files is `pi`. This single board computer fits as well as the H-bridge driver into the train. The system is powered by the Lego Power Functions battery box. A 5V buck converter is needed for supplying the Raspberry Pi.

## Hardware
- Raspberry Pi Zero
- Lego Power Functions battery box
- Lego Power Functions train motor
- H-bridge (TB6612FNG)
- Raspberry Pi camera (optional)

## Pinouts/hookup guides
- [Raspberry Pi](https://pinout.xyz/)
- [H-bridge (TB6612FNG)](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide?_ga=2.26950901.915922753.1659629747-1165382823.1659533506)
- [Lego Power Functions](https://scuttlebots.com/2014/03/02/lego-pf-hacking-wiring/)

## Connections
### Lego Power Functions battery box <-> buck-converter
| Battery box pin | Buck pin | Purpose            |
|:----------------|:---------|:-------------------|
| 9V              | IN+      | Input voltage |
| GND             | IN-      | Ground             |

### Lego Power Functions battery box <-> H-bridge
| Battery box pin | H-bridge pin | Purpose       |
|:----------------|:-------------|:--------------|
| 9V              | VM           | Motor voltage |
| GND             | GND          | Ground        |

### Buck-converter <-> Raspberry Pi
| Buck pin | Raspi pin | Purpose           |
|:---------|:----------|:------------------|
| OUT+     | 5V        | Supply voltage    |
| OUT-     | GND       | Ground            |

### Raspberry Pi <-> H-bridge
| Raspi pin | H-bridge pin | Purpose           |
|:----------|:-------------|:------------------|
| 3.3V      | VCC          | Logic voltage     |
| GND       | GND          | Ground            |
| GPIO14    | AIN1         | Motor direction 1 |
| GPIO15    | AIN2         | Motor direction 2 |
| GPIO18    | PWMA         | PWM (motor speed) |
| GPIO23    | STBY         | Standby           |

### H-bridge <-> LPF motor
| H-bridge pin | LPF motor pin | Purpose           |
|:-------------|:--------------|:------------------|
| A01          | C1            | Motor direction 1 |
| A02          | C2            | Motor direction 2 |


## Installation
Install paho-mqtt library:
```
sudo pip install paho-mqtt
```

Clone this repository:
```
git clone https://github.com/ElectroSheepH21/Raspi-Cam-Controller.git
```
> **Note**
> Clone the repository into the user directory otherwise you have to update the paths in the files of this repository
> 
> **Note**
> Make sure to update the files of this repository if your username differs from `pi`

Navigate to the repository:
```
cd /home/username/Python-TrainLPF-MQTT
```
> **Note**
> Substitute `username` with your username

Run the main script:
```
python main.py
```

## Run the MQTT client at startup (recommended)
Make main.py an executable:
```
chmod +x main.py
```

Copy the MQTT service file to the system service files:
```
sudo cp trainlpf-mqtt.service /etc/systemd/system
```

Reload systemctl:
```
sudo systemctl daemon-reload
```

Test the MQTT service file:
```
sudo systemctl start trainlpf-mqtt.service
sudo systemctl status trainlpf-mqtt.service
```
> **Note**
> If the systemctl status comand fails, check and update the paths in the files of this repository

Enable the MQTT service file:

```
sudo systemctl enable trainlpf-mqtt.service
```

## Install mjpg-streamer (optional)
Configure camera:
```
sudo raspi-config
```
#### Interface Options --> Legacy Camera
Clone the repository:

```
git clone https://github.com/jacksonliam/mjpg-streamer.git
```

Install cmake:
```
sudo apt install cmake -y
```

Install JPEG image codec library:
```
sudo apt install cmake libjpeg62-turbo-dev -y
```

Install gcc and g++ compiler:
```
sudo apt install gcc g++ -y
```

Build and install all plugins that can be compiled:
```
cd /home/username/mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
```
> **Note**
> Substitute `username` with your username

## Run the mjpg-streamer at startup (optional)
Navigate to the repository:
```
cd /home/username/Python-TrainLPF-MQTT
```
> **Note**
> Substitute `username` with your username

Copy the mjpg-stream service file to the system service files:
```
sudo cp mjpg-stream.service /etc/systemd/system
```

Reload systemctl:
```
sudo systemctl daemon-reload
```

Test the MQTT service file:
```
sudo systemctl start trainlpf-mqtt.service
sudo systemctl status trainlpf-mqtt.service
```
> **Note**
> If the systemctl status comand fails, check and update the paths in the files of this repository

Enable the MQTT service file:
```
sudo systemctl enable trainlpf-mqtt.service
```
