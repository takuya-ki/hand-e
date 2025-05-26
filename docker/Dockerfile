FROM ros:noetic

RUN apt update && apt install -y --no-install-recommends curl lsb-release wget gnupg
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xC1CF6E31E6BADE8868B172B4F42ED6FBAB17C654' | apt-key add -

# setting environmental variables
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && apt install -y --no-install-recommends tzdata
RUN apt update -y && apt install -y --no-install-recommends \
    ros-noetic-desktop-full \
    ros-noetic-image-proc \
    ros-noetic-image-view \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-control-toolbox \
    ros-noetic-moveit \
    ros-noetic-moveit-visual-tools \
    ros-noetic-effort-controllers \
    ros-noetic-forward-command-controller \
    ros-noetic-joint-state-controller \
    ros-noetic-joint-trajectory-controller \
    ros-noetic-position-controllers \
    ros-noetic-velocity-controllers \
    ros-noetic-tf \
    ros-noetic-tf2-tools \
    ros-noetic-robot-state-publisher \
    ros-noetic-joint-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-genpy \
    ros-noetic-industrial-core \
    ros-noetic-roslint \
    ros-noetic-ddynamic-reconfigure \
    ros-noetic-urdf-tutorial \
    ros-noetic-socketcan-interface \
    ros-noetic-soem \
    python3-osrf-pycommon \
    python3-catkin-tools \
    python3-rosdep \
    python3-pip \
    python3-tk \
    software-properties-common \
    build-essential \
    libxkbcommon-x11-0 \
    libcanberra-gtk* \
    libgl1-mesa-dev \
    libudev-dev \
    libxcb* \
    xorg-dev \
    net-tools \
    psmisc \
    byobu \
    dbus \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/
RUN mkdir -p /catkin_ws/src && \
	/bin/bash -c "cd /catkin_ws/src && source /opt/ros/noetic/setup.bash && catkin_init_workspace" && \
	/bin/bash -c "cd /catkin_ws && source /opt/ros/noetic/setup.bash && catkin build" && \
	echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
	echo "source /catkin_ws/devel/setup.bash" >> ~/.bashrc && \
	echo "export ROS_PACKAGE_PATH=\${ROS_PACKAGE_PATH}:/catkin_ws" >> ~/.bashrc && \
	echo "export ROS_WORKSPACE=/catkin_ws" >> ~/.bashrc

WORKDIR /
RUN wget -P /opt https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh && \
    bash /opt/Anaconda3-2020.02-Linux-x86_64.sh -b -p /opt/anaconda3 && \
    rm /opt/Anaconda3-2020.02-Linux-x86_64.sh && \
    export PATH=/opt/anaconda3/bin:$PATH && \
    . ~/.bashrc && conda init && conda update -n base -c defaults conda

RUN pip3 install --target=/opt/ros/noetic/lib/python3/dist-packages rospkg
RUN rm /etc/apt/sources.list.d/ros1-latest.list
RUN . ~/.bashrc && conda deactivate && pip3 uninstall netifaces -y && pip3 install netifaces==0.11.0 serial

# gazebo on ros1
WORKDIR /catkin_ws/src/
RUN git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins.git && \
    cd roboticsgroup_gazebo_plugins && \
    git reset --hard 509a32e

RUN pip3 install --force-reinstall "setuptools==65.5.1" "importlib_metadata==6.0.1"

WORKDIR /cakin_ws/src/
RUN pip3 install git+https://github.com/tingelst/robotiq_modbus_controller.git --upgrade
RUN pip3 install pymodbus==3.0.2 pyserial==3.5

# Generate bash commands
WORKDIR /catkin_ws/
RUN echo "source /opt/ros/noetic/setup.bash && cd /catkin_ws && catkin build -DPYTHON_EXECUTABLE=/usr/bin/python3 && bash" >> ~/.bash_history
RUN echo "rosservice call /hande/set_command \"command: 'c'\"" >> ~/.bash_history
RUN echo "rosservice call /hande/set_command \"command: 'o'\"" >> ~/.bash_history
RUN echo "roslaunch hande_tutorials server.launch is_real:=False" >> ~/.bash_history
RUN echo "roslaunch hande_tutorials server.launch is_real:=True" >> ~/.bash_history
RUN echo "roslaunch hande_tutorials demo.launch is_real:=False" >> ~/.bash_history
RUN echo "roslaunch hande_tutorials demo.launch is_real:=True" >> ~/.bash_history
RUN echo "roslaunch hande_description display.launch" >> ~/.bash_history