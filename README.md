Research designated, data collection software designed for IoT Technology Lab for Northeastern's "HomeLab". This software will generate a server and GUI to manage a cutting edge set of IoT sensors. Our platform also supports cameras, live data viewing, sensor data storage, data export, and live sensor map.

Containers include Zigbee2Mqtt, Z-waveJSUI, Fast-API, MariaDB, Frigate, HomeAssistant, MQTT, ESPHome.

HomeLab Report: [https://docs.google.com/document/d/18Yx7UeD4_WpNmbq7Nc6DwJqMMfXya9Zz113vEpatAVk/edit?usp=sharing](https://docs.google.com/document/d/1eoux5RwuEPGIoL_3dLIfYjpPR9ozhAaJkfLdJ7A7VqM/edit?usp=sharing)
HomeLab FAQS: https://docs.google.com/document/d/18Yx7UeD4_WpNmbq7Nc6DwJqMMfXya9Zz113vEpatAVk/edit?tab=t.ux6u23mv5h61

------------------------------------------------------------------------------------------------------------------------------------

For setup: (Linux Ubuntu machine required)
1. Clone Repo
2. Download Docker Engine
3. In HomeLab_Compose -----> "docker-compose up"

Common Issue:
Zigbee requires specifiying the usb port of the cordinator, so this will need to be manually adjusted -----> "ls -l /dev/serial/by-id".
Z-wave will adjust automatically.

HomeAssistant is a fantastic IoT integration platform and will provide the majority of functionality. Access is available through localhost:8123 
User: "Cole" 
Password: "aaa$aaa"
A designated linux server will run this. Computers on the same network can access all technology tools and data access. 

The containers start via dockercompose.yaml, which is where all the container setting can be adjusted. These containers are already preset to be viewable (ported) as a tab in HomeAssistant. These tabs include Sensor Configuring (Zigbee2Mqtt & Z-waveJSUI), Cameras (Frigate), and Database Export (Fast-API).




