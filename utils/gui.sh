#!/bin/bash

byobu new-session -d -s bringup
byobu select-pane -t 0
byobu split-window -v
byobu select-pane -t 0
byobu split-window -h
byobu select-pane -t 2
byobu split-window -h
byobu select-pane -t 2

byobu send-keys -t 0 'roscore' 'C-m'
sleep 2.
byobu send-keys -t 1 'rosparam set /device /dev/ttyUSB0; rosrun robotiq_2f_gripper_control Robotiq2FGripperRtuNode.py' 'C-m'
sleep 2.
byobu send-keys -t 2 'rosrun robotiq_2f_gripper_control Robotiq2FGripperSimpleControllerRviz.py' 'C-m'
sleep 2.
byobu send-keys -t 3 'roslaunch robotiq_2f_hande_visualization robotiq_2f_hande_model.launch' 'C-m'

byobu attach -t bringup
