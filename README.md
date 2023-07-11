# hand-e

[![support level: community](https://img.shields.io/badge/support%20level-community-lightgray.svg)](http://rosindustrial.org/news/2016/10/7/better-supporting-a-growing-ros-industrial-software-platform)
[![License: Apache](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![License: BSD](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![repo size](https://img.shields.io/github/repo-size/takuya-ki/hand-e)

ROS meta package based on [ros-industrial/robotiq](https://github.com/ros-industrial/robotiq).

## Requirements

- [Ubuntu 18.04 PC](https://ubuntu.com/certified/laptops?q=&limit=20&vendor=Lenovo&vendor=Dell&vendor=HP&release=18.04+LTS)
    - [ROS Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu)
    - [Byobu](https://www.byobu.org/)

## Installation

```bash
mkdir -p catkin_ws/src && cd catkin_ws
git clone https://github.com/takuya-ki/hand-e.git src
rosdep install --from-paths src --ignore-src --rosdistro=melodic -y --os=ubuntu:bionic
sudo apt update && sudo apt install ros-melodic-joint-state-publisher-gui byobu
catkin build
source catkn_ws/devel/setup.bash
```

## Usage

1. Connect the Hand E with usb cable to the controll computer
2. Prepare the execution
```bash
sudo usermod -a -G dialout username
ls -l /dev/ttyUSB0
sudo chmod +777 /dev/ttyUSB0
```

3. Execute a script

### [Interactive control](https://wiki.ros.org/robotiq/Tutorials/Control%20of%20a%202-Finger%20Gripper%20using%20the%20Modbus%20RTU%20protocol%20%28ros%20kinetic%20and%20newer%20releases%29)
```bash
./utils/gui.sh.
```

### A demonstration script
```bash
./utils/demo.sh
```

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)
