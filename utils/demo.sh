#!/bin/bash

byobu new-session -d -s bringup
byobu select-pane -t 0
byobu split-window -v
byobu select-pane -t 0
byobu split-window -h
byobu select-pane -t 2
byobu split-window -h

byobu send-keys -t 0 'roscore' 'C-m'
sleep 2.
byobu send-keys -t 1 'rosrun robotiq_2f_gripper_control Robotiq2FGripperRtuNode.py _device:=/dev/ttyUSB0' 'C-m'
sleep 2.
byobu send-keys -t 2 'rosrun robotiq_2f_gripper_control Robotiq2FGripperSimpleControllerServer.py' 'C-m'
sleep 2.
byobu send-keys -t 3 'rosservice call /hand_e/set_command r' 'C-m'
sleep 2.
byobu send-keys -t 3 'rosservice call /hand_e/set_command a' 'C-m'
sleep 2.
byobu send-keys -t 3 'rosservice call /hand_e/set_command c' 'C-m'
sleep 2.
byobu send-keys -t 3 'rosservice call /hand_e/set_command o' 'C-m'

byobu attach -t bringup
