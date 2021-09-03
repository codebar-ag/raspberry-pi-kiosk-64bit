# Setup Raspberry Pi

## Hardware

```
- Raspberr Pi Official USB-C Power Supply
- Raspberry PI 4 Computer, Model B 8GB RAM
- PureLink CInema Seriers Micro HDMI - HDMI Cable (CS1200-030)
- M2.SDD via USB-3.0
```

## Image

```
https://downloads.raspberrypi.org/raspios_arm64/images
```

**Note:** Do make sure to use arm not armhf imges.

## SSH-Access

```
Add an empty ssh file within the boot folder of the image.

host => raspberrypi.local
username => pi
paswword => raspberry

ssh pi@raspberrypi.local

```

### Remove local cached fingerpint for IP on your device

```
ssh-keygen -R 192.168.1.2
```

## Settings (manually)

```
Ddisable Sleep Mode Dispaly
```

# Firmeware Update

```
sudo apt-get upgrade -y
sudo rpi-eeprom-update
sudo rpi-eeprom-update -a
```

## Installation

### Prerequisites

#### Install Chromedriver and Selenium

- pre Updates

```
sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

```

- Install chromedriver

Get Chromedriver from electron GitHub release. Make sure it supports the installed chromium version on your Pie!
Make sure you downloaded the right os version. ARM64 Tipp: To get versions Enter `chromium --product-version`
Or `chromedriver --product-version`
after download unzip

# Driver

```
sudo wget https://github.com/electron/electron/releases/download/v12.0.18/chromedriver-v12.0.18-linux-arm64.zip
unzip chromedriver-v12.0.18-linux-arm64.zip
```

Make sure to configure ChromeDriver on your system (move the chromedriver to /usr/lib)

```
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

sudo reboot

```

After this everything should be set up. In case you installed the wrong version of chromedriver. removing chrome driver:

```
sudo rm -f /usr/bin/chromedriver 
sudo rm -f /usr/local/bin/chromedriver 
sudo rm -f /usr/local/share/chromedriver
``` 

helpful sources:
LinkOne(https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/)
LinkTwo(https://patrikmojzis.medium.com/how-to-run-selenium-using-python-on-raspberry-pi-d3fe058f011)
_This could need a bit more improvment, if you run in to problems -> @TrevisGordan_

### Clone Github Repository

Make sure you have a ssh public key and have access to the repository

```
ssh-keygen
cat ~/.ssh/id_rsa.pub

git clonehttps://github.com/codebar-ag/raspberry-pi-kiosk
```


### Install Pyhton Dependencies

install all python dependencies. on raspi os explicitly use 'python3' & 'pip3' commands to call python. run:

```
pip3 install -r requirements.txt
```

### Set Up the Config.

To use autostart config has to be set up correctly.
_NOTE! SECRETS SHOULD NOT BE VISIBLE IN GIT AND USED WITH ENV VARS._

Add the Enviroment Variable AUTH_TOKEN with the right AuthToken to CWD. In Terminal at (CWD, where the autostart.py is).

```
cp .env.dist .env
export AUTH_TOKEN="YOUR_TOKEN"
```

or create a .env file inside the CWD. place the ENV Var their. the Config script will automaticly load the token. from
the config.yaml.

#### Configuration

```
sudo raspi-config
```

#### GL Driver

Advanced Options / GL Driver / G2 GL (Fake KMS)

#### Enable the compositor.

Advanced Options / Compositor / Yes

### Chrome

### Plugins 
Chromium on Raspberry Pi OS comes with uBlock Origin and h264ify extensions installed by default. Make sure that h264ify
is enabled, so YouTube uses h264-encoded videos for which the Raspberry Pi supports hardware-accelerated video decode.

```
https://www.linuxuprising.com/2021/04/how-to-enable-hardware-acceleration-in.html
https://medium.com/for-linux-users/how-to-make-your-raspberry-pi-4-faster-with-a-64-bit-kernel-77028c47d653
```

#### Flags

```
chrome://flags/#enable-accelerated-video-decode
chrome://flags/#ignore-gpu-blocklist
```

### Autostart

```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

*WARNING*: The (CWD) Current Working Director the autostart directory!
Change on Directory up to autostart

```
cd /home/pi/Scripts/autostart/
```

then run with python3

```
python3 autostary.py
```

- autostart will open the chromium in Fullscreen kioskmode.

_TIPP: To exit the kioskmode close it with ALT+F4_
