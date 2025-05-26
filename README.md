# hand-e

[![support level: community](https://img.shields.io/badge/support%20level-community-lightgray.svg)](http://rosindustrial.org/news/2016/10/7/better-supporting-a-growing-ros-industrial-software-platform)
![repo size](https://img.shields.io/github/repo-size/takuya-ki/hand-e)

ROS Noetic package for Robotiq Hand-E gripper.

## Dependency (tested as a host machine)

- [Ubuntu 22.04 PC](https://ubuntu.com/certified/laptops?q=&limit=20&vendor=Dell&vendor=Lenovo&vendor=HP&release=22.04+LTS)
  - Docker 26.1.1
  - Docker Compose 2.27.0

## Installation

```bash
git clone git@github.com:takuya-ki/hand-e.git -b noetic-devel --recursive --depth 1 && cd hand-e && COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose build --no-cache --parallel 
```  
1. Build and run the docker environment  
   - Create and start docker containers in the initially opened terminal  
        ```bash  
        docker compose up  
        ```  
   - Execute the container in another terminal  
        ```bash  
        xhost + && docker exec -it hande_noetic_container bash  
        ```  
        ```bash  
        sudo usermod -a -G dialout username && ls -l /dev/ttyUSB0 && sudo chmod +777 /dev/ttyUSB0  
        ```  
2. Build program files with the revised yaml  
    ```bash  
    cd /catkin_ws && cakin build -DPYTHON_EXECUTABLE=/usr/bin/python3 && source devel/setup.bash  
    ```  
3. Run a planning process in the container  
   - Use byobu to easily command several commands  
        ```bash  
        byobu  
        ```  
        - First command & F2 to create a new window & Second command ...  
        - Ctrl + F6 to close the selected window  

##### Display the robot's (visual and collision) models  
```bash
roslaunch hande_description display.launch
```
- Robot Visual  
<img src="images/visual.png" height="200">  
- Robot Collision  
<img src="images/collision.png" height="200">  

##### Run the hand closing and opening demonstrations in simulations
```bash
roslaunch hande_tutorials demo.launch is_real:=False
```

##### Run the hand closing and opening demo in the real world  
```bash
roslaunch hande_tutorials demo.launch is_real:=True
```

##### Run the server receiving motion commands in simulations
```bash
roslaunch hande_tutorials server.launch is_real:=False
rosservice call /hande/set_command "command: 'o'"
rosservice call /hande/set_command "command: 'c'"
```

##### Run the server receiving motion commands in the real-world
```bash
roslaunch hande_tutorials server.launch is_real:=True
rosservice call /hande/set_command "command: 'c'"
rosservice call /hande/set_command "command: 'o'"
```

## Contributors

We always welcome collaborators!

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)
