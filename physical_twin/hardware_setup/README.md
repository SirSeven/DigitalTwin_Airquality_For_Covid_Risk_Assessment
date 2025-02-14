# Setup Physical Twin with actual hardware

## Contents
- [Prerequisites](#Prerequisites)
- [Hardware setup](#Hardware_setup)
	- [Raspberry Pi](#Raspberry)
	- [Raspberry Pico](#RaspberryPico)
	- [Sensor CCS811](#ccs811)
	- [Sensor SCD30](#scd30)
- [Initial Setup of Raspberry OS](#Initial_Setup_of_Raspberry_OS)
- [Initial Setup of Arduino Uno](#Initial_Setup_of_Arduino_Uno)
- [Send Sensor data to cloud](#Send_Sensor_data_to_cloud)
	- [Required Libraries for the project](#libraries)
	- [Remote access via SSH](#ssh)
	- [Deploy script for sending data to web-server](#Deploy)
	- [Deploy script for sending data to IoT-hub](#Sending)
- [Possilble Frequent Errors](#Possilble_Frequent_Errors)

## <a name="Prerequisites"></a>Prerequisites
- Raspberry and accessories
- Arduino and accessories
- CCS811 and DHT11 Sensors
- Electronics like resistors, LED lights 
- Bread board and connection wires

## <a name="Hardware_setup"></a>Hardware setup
### <a name="Raspberry"></a>Raspberry Pi
 We ue [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) boards. Raspberry is a dedicated computer with all neccesary functions just like an ordinary pc.  The raspberry sends measured CO<sub>2</sub> values to the cloud and is also used to command the treshold triggers if the values reach above the limit by changing the color of the LED or by Beeping sounds.
 
 <img src='https://cdn.idealo.com/folder/Product/6628/1/6628198/s2_produktbild_max/raspberry-pi-4-model-b.jpg'  width=400 />
 
 An alternative would be NVIDIA's [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit). However in this project a Raspberry is used and for this following hardware for setting up the raspberry is needed:
- (Fully Integrated) Raspberry Pi 4 - Board
- Power adapter for Raspberry Pi 4 (USB-C)
- SD-card
- LAN-cable
- Card-Reader (for initialization)
- Keyboard (for initialization)
- Micro-HDMI to HDMI cable (for initialization)


#### <a name="RaspberryPico"></a>Raspberry Pico
 Another alternative to the Raspberry Pi 4 would be using the Raspberry Pico which is slightly cheaper than the Raspberry Pico. 
 
<img src='https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/blob/main/physical_twin/hardware_setup/images/pin_layout.jpg'>

### <a name="ccs811"></a>Sensor CCS811 
- This [Adafruit CCS811](https://joy-it.net/en/products/SEN-CCS811V1) sensor is using the I2C protocol
- It has Measurement range: 400 ppm – 8192 ppm for CO<sub>2</sub> values
- To get valid data a initial burn-in of 48 hours and a warm-up time of 20 min is recommended.
- There are datasheet and manual available at the homepage of joy-it. The manual also includes an example of how to access the sensor in code. A short summary is available in (subsection - 1.6.4) datasheet documentation and manual are located at the repository for further information.
- Wiring scheme:

 
| sensor pin 	| property  	| Raspberry GPIO/pin  	|
|------------	|------------	|------------	|
| vdd        	| +5v        	|`pin2`				|
| gnd        	| Ground     	|`pin6`|
| sda        	| data line  	|`gpio2`|
| scl        	| clock line 	|`gpio3`|
| Rst        	| Reset port 	|`pin39`|

<img align="center" src="https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png" width= 400/>

### <a name="scd30"></a>Sensor SCD30
-  SCD30 - Sensor Module for HVAC and Indoor Air Quality Applications. it has Integrated temperature and humidity sensor
-  It has Measurement range: 400 ppm – 10.000 ppm for CO<sub>2</sub> values
-  works with Digital interface UART or I2C modules
-  further documentation can be found under this [homepage](https://www.sensirion.com/en/environmental-sensors/carbon-dioxide-sensors/carbon-dioxide-sensors-scd30/)

| sensor pin 	| property  	| Raspberry GPIO/pin |
|------------	|------------	|------------	|
| vdd        	| +3v        	|`pin1`|
| gnd        	| Ground     	|`pin6`|
| sda        	| data line  	|`gpio2`|
| scl        	| clock line 	|`gpio3`|
| Rst        	| Reset port 	|`pin39`|

<img align="center" src="https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png" width= 400/>

## <a name="Initial_Setup_of_Raspberry_OS"></a>Initial Setup of Raspberry OS 
After having the new Raspberry or when Need to flash old raspberry to install new  Ubuntu.
Required Things:
1. Brand new Raspberry / Raspberry that need to be flashed new
2. Download thePi Imagerfile and install it from [this link](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#)
3. If your in Linux InstallPi Imagerby following the command
```sh
 sudo snap install rpi-imager
```
4. choose the OS as [Raspberry pi OS](https://www.raspberrypi.org/software/) 32 bitprobably it will be in first option

<img align="center" src="https://www.raspberrypi.org/app/uploads/2020/03/RPI_intro-e1583228263677.png" width= 400/>

6. insert the sd card and click write
7. After it has been installed you can insert this sd card into raspberry and you have an updated version of linux
    installed on you device.

For the setup of the Raspberry Pi an introduction is given on the Raspberry Pi's official homepage. In the following section a short overview is given. First of all an operating system needs to be downloaded and an image needs to be installed on the SD-card. For this step the Card-Reader is needed. For this project the Raspberry Pi OS Lite (32-bit) is used, which is a port of Debian with no desktop environment. There is an Imager program available to speed up the installation step. The instructions of the program need to be followed and afterward the SD-Card is ready to use. The next step is to connect the Raspberry Pi (Power adapter, LAN-cable, Keyboard and HDMI cable) and to insert the SD-Card. The initial startup is done and thedefault login data is:

- user: pi
- password: raspberry

A few setting needs to be done initially, therefore enter the command:
```sh
sudo raspi-config
```
into the console. The following settings had been changed:

- System Options - Password: the password has been changed tocdl, the username remains  the same 
- System Options - Hostname: the hostname has been changed torpi-cdl(this name will
    be needed later to get the IP of the Raspberry Pi without a monitor)
- Interfacing Options - SSH: enable remote command line access to the Raspberry Pi via SSH
- Interfacing Options - I2C: enable I2C interface and loading the I2C kernel module automatically (will be needed for some of the used sensors)

Afterward the Raspberry Pi needs to be restarted and logged in with the new password. To be sure that the OS and its programs are up-to-date the following commands need to be executed:
```sh
sudo apt-get update
sudo apt-get upgrade
```



### To Enable SSH without using Monitor:
To setup raspi without hdmi this is the process:

first flash the sd card with new pi OS. Then Power off your Raspberry Pi and remove the SD card. and follow thes

1.  Insert the SD card into your computer’s card reader. The SD card will mount automatically.
2.  Navigate to the SD card boot directory using your OS file manager. Linux and macOS users can also do this from the command line.
3.  Create a new empty file named ssh, without any extension, inside the boot directory.
4.  Remove the SD card from your computer and put it in your Raspberry Pi.
5.  Power on your Pi board. On boot Pi will check whether this file exists and if it does, SSH will be enabled and the file is removed.

### Connecting Raspi by SSH (without knowing IP address): 
**Using your computer & Ping command**

1.  Connect your computer to the same Network as Raspberry Pi
2.  Open a terminal window (Command Prompt on Windows)
3.  Run the following command `ping raspberrypi.local` (If you have changed the default hostname of your Raspberry Pi, type `ping YOUR_HOSTNAME.local` instead)
    
    > Note: On Windows PC, mDNS driver is required for .local addresses to work, you may install this service: [https://support.apple.com/kb/DL999?locale=en_US 761](https://support.apple.com/kb/DL999?locale=en_US "https://support.apple.com/kb/dl999?locale=en_us")
    
4.  If the Raspberry Pi is reachable, ping will show its IP address, e.g:  
    `PING raspberrypi.local (192.168.1.33): 56 data bytes`  
    `64 bytes from 192.168.1.33: icmp_seq=0 ttl=255 time=2.618 ms`
	
### If you want to connect raspi To WIFI without monitor:
If you already flashed raspi with new os or cant connect to monitor use this step to connect to wifi automatically.

1.  Remove the sd card and plug in any of your pc
2.  navigate to the particular mount: under boot create a 'wpa_supplicant.txt' file
3.  open it and add these texts
4.  ```bash
    country=US # Your 2-digit country code
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    network={​​​​​
        ssid="YOUR_NETWORK_NAME"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }​​​​​
    ```
    
5.  Save the file with your wifi ssid=' ' and password = ' '
6.  Finally just chanage the file extention from .txt to .conf

This will connect the raspi to wifi right after starting, No monitor is needed. you can do it right after flasing the os


### <a name="libraries"></a>Required Libraries for the project

Now, you need to install some packages with the integrated package installer of Pythonpip.
The Required packages are as follows:
- RPi.GPIO
- Adafruit-DHT
- adafruit-circuitpython-ccs811CO<sub>2</sub>
- azure-iot-device
- SCD30

Execute all these commands one by one each:
```py
# Packages to be Installed
python3 -m pip install RPi.GPIO		#For GPIO
python3 -m pip install Adafruit-DHT		#For DHT sensor
python3 -m pip install adafruit-circuitpython-ccs811	#For CCS811 sensor
python3 -m pip install azure-iot-device		#For installing azure
python3 -m pip install scd30_i2c	#For SCD_30 sensor

# Dependent Packages (Probably all should be pre-installed)
pip install json
pip install urllib3
pip install DateTime 
sudo apt-get install -y python-requests
```

### <a name="ssh"></a>Remote access via SSH

It is planned that the AirQuality module will be running continuously in a predefined position (e.g.: in the stairway below the TV), therefore it needs to be accessible remotely without any connected monitor and input device. To solve this requirement, the Raspberry Pi can be accessed via SSH which can be enabled insudo raspi-configas mentioned in subsection. The IP address of the Raspberry Pi can be set as static, to ensure the connection to it. It is also possible to get the IP address with apingcommand on the hostname of the Raspberry Pi from another computer. For Linux it is easy as entering the following command.
```py
syntax:
ping <pi_hostname>.local
```
For Windows it is needed to add the parameter -4 to the ping command, so that the resolved IP address is in the IPv4 format.
```sh
ping rpi-cdl.local
```
With this IP address it is easy to access the Raspberry Pi with an SSH capable tool like
putty. Figure 1.2 shows a screenshot of the applicationputtywith the local IP address of the Raspberry Pi, the Port 22 and the connection type SSH marked. These settings can be saved and used for later access. If the Raspberry Pi was connected over another LAN-connection, the IP address would have needed to be updated.


### <a name="Deploy"></a>Code deployment for sending data to custom web server

>1. Note: Before continuing to procedures make sure you have all the packages installed in your deploying machine. To do so refer the topic above_ [Required Libraries for the project](#libraries)
>2. Cutom web server should already setup and url and content should be ready 

To deploy the _Data Abstraction_ script which sends data to cloud we use `auto_deploy_script.py`  which does following process when trigered:
1. Deploy the data abstraction script on each client device
2. Start the data abstraction script to send the data

Please follow the procedure below: 

1. There will be file `devices_list.txt` created if not just create one. Enter the details of all devices as in the format given below. required deatils parameters are:         `Data_abstract_script, Ip address, User_id, Password, Device_id`

```txt
'IoTHubDevice.py', '140.78.42.100', 'pi1', 'cdl', 'Rasp01'
'IoTHubDevice.py', '140.78.42.102', 'pi2', 'cdl', 'Rasp02'
<add the as many devices with same syntax>
```
>Note: Inside the IoTHubDevice.py you can specify the endpoint details (i.e. server url and content format as mentioned below)
```py
# Details of custom web server 
url="<your web-server url>"
headers = {'<content-type>','Accept':'application/json'}
```

2.  After list is saved, automation script named `auto_deploy_script.py`. you can run it using python3 using command:
```py
# For deploying script to clients
python3 auto_deploy_script.py 
```
	Note: This process will be asking password for each raspberry you can type in console consequtively.

This will copy all required scripts from host server to the clients (raspberry) and trigers the script to start send the data web server.

  
### <a name="Sending"></a>Code deployment for sending data to Azuer IoT-hub
>_Note: Before continuing to procedures make sure you have all the packages installed in your deploying machine. To do so refer the topic above_ [Required Libraries for the project](#libraries)

Steps to follow:
1. Just edit the list in `device_list.txt` with requried details of ip address and much more. List all of the devices.

3. Make your azure environemnt is already setup to make it ready for receiving our data. Here is tutorial on how to set up the azure environment is found here: [IndoorAirQuality_DigitalTwin_Exemplar/digital_twin/azure/readme.md](https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/tree/main/digital_twin/azure)

4. Inside `IoTHubDevice.py` set the connection string varibale to appropriate string accoding to [azure IoT-Hub readme.md](https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/tree/main/digital_twin/azure). And it should be unique for each devices in IoT-Hub for example:
```py
# Connection string from IoT-Hub Devices list from Azure
CONNECTION_STRING_CCS811 = "<specify the connection string>"
CONNECTION_STRING_SCD_30 = "<specify the connection string>"
```

> Note: in IoTHubDevice.py please make sure you have updated `connection_string` from your azure portal: under iot-hub/iot-devices for sending the data from raspberry. further notes can be found under Setup `IoT-Hub`  in [IndoorAirQuality_DigitalTwin_Exemplar/digital_twin/azure/](https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/tree/main/digital_twin/azure). 

3. This will get ready to script to send the data (Note: data is not yet sent to cloud). Refer [Sending data to IoT-Hub](#Sending) to start sending the data.
4. run the auto_deploy_script with the syntax:
```py
# Deploy code to clients
python3 auto_deploy_script.py
```
5.  This will deploy the code and also trigger the code and runs it continuously without interuptions so the data is sent constantly.


## <a name="Possilble_Frequent_Errors"></a>Possilble Frequent Errors
###### Error: `Script not running in raspberry`:
Make sure you have the updated OS and all lybraries installed and make sure the script is running in `python v3` not in v2

###### Error: `Runtime Errror`: 
Baud Rate of device and sensor isn't matching preferred one is `Baud Rate = '100000'` kHz. process to change is decribed above.

###### Error: `Device not Found`:
Wiring is not good for sensor. you can always check the sensor is in connection by the command:
```sh
sudo i2cdetect -y 1
```
This will show if the device is connected or not. Further detailed discription is under [this link](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

###### Error: `Try Reapplying the voltage`:
Some wiring connection problem

###### Error: `Constant CO<sub>2</sub> value`:
Sensor is not sensing good or sensor calibration is needed.
###### Error: `Data not receieved on Azure`:
Connection string is bad or no device is to receive the data from Azure side



