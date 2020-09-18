# Autonomous RC Car - Raspberry Pi | Python & C

Constructing an RC Car to drive autonomously or controlled via remote operations such as a mobile device (Web server) or an infrared remote sensor (Receiver).

Features to include but not limited to:
- Autonomous surveillance of local area
- Guild line trailing and pathing
- Facial recognition
- Ultrasonic distance sensor
- Temperature & Humidity | Barometric Pressure | Gyroscope sensors

<ins>Parts to Order</ins>
- [4WD Robot Chassis RC](https://www.amazon.com/gp/product/B07F759T89/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) ✔
- [L298N Dual H Bridge Motor Driver Controller](https://www.amazon.com/gp/product/B01M29YK5U/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) ✔
- 5MP Camera Module ✔
  - https://www.ebay.com/itm/5MP-Camera-Module-Webcam-Video-1080p-Transparent-Holder-For-Raspberry-Pi-3B-2B/372630446368?_trksid=p2485497.m4902.l9144
- Ultrasonic Distance Sensor ✔
  - https://www.ebay.com/itm/10Pc-Distance-Measuring-Transducer-Sensor-for-Arduino-HC-SR04-Ultrasonic-Module/182898071023?_trksid=p2485497.m4902.l9144

## Current Prototype Build
<img src="/assets/images/rc_structure.jpg" width="50%">

### Features:
- Ultrasonic Distance Sensor
- Temperature & Humidity
- LED for beacon and object detection
- Web rendered grid for mapping of local environment in a 5x5 grid.

<img src="/assets/images/rc_web_grid.PNG" width="50%">

### Grid Color Recognition:
- Cyan border color is the current position of the RC Car.
- Green border is the chosen destination (Manual).
- Orange circle border denotes an object within that sector.
- Red border represents temperatures > 32° C or ~89° F
- Shaded border is for visited sectors.
