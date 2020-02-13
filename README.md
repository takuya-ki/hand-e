# hand-e

Implementation of Robotiq Hand-E.

## Requirements

- Ubuntu 18.04
- ROS melodic

## Installation

    $ mkdir -p catkin_ws/src && cd catkin_ws
    $ catkin build
    $ cd src 
    $ git clone https://github.com/takuya-ki/hand-e.git
    $ cd ..
    $ rosdep install --from-paths src --ignore-src --rosdistro=melodic -y --os=ubuntu:bionic
    $ catkin build

[Important issue](https://github.com/ros-industrial/robotiq/issues/159)

## Usage

   # connect the Hand E with usb cable to the controll  computer
   
#### [Interactive control](https://wiki.ros.org/robotiq/Tutorials/Control%20of%20a%202-Finger%20Gripper%20using%20the%20Modbus%20RTU%20protocol%20%28ros%20kinetic%20and%20newer%20releases%29)

   $ sudo usermod -a -G dialout username
   $ ls -l /dev/ttyUSB0
   $ sudo chmod +777 /dev/ttyUSB0
   $ roscore
   $ rosrun robotiq_2f_gripper_control Robotiq2FGripperRtuNode.py /dev/ttyUSB0
   $ rosrun robotiq_2f_gripper_control Robotiq2FGripperSimpleController.py

   $ roslaunch robotiq_2f_85_gripper_visualization test_2f_85_model.launch 
   $ roslaunch robotiq_2f_140_gripper_visualization test_2f_140_model.launch 
   $ roslaunch robotiq_2f_c2_gripper_visualization test_robotq_c2_model.launch 

#### TODO: We can use the robotiq_hande_gripper_discription in the robotiq_modular_gripper

## Author

[Takuya Kiyokawa](https://takuya-ki.github.io/)
