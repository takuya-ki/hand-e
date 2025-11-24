FROM ubuntu:22.04

# setting environmental variables
ENV DEBIAN_FRONTEND noninteractive

# Timezone and Launguage
RUN apt update -y && apt install -y --no-install-recommends \
    software-properties-common \        
    locales \
    tzdata \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
    && add-apt-repository universe

ENV LANG en_US.UTF-8
ENV TZ=Asia/Tokyo

RUN apt update -y && apt install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    lsb-release \
    python3-pip \
    python3-tk \
    gnupg2 \
    byobu \
    curl \
    wget \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update -y && apt install -y --no-install-recommends \
    ros-humble-desktop \
    ros-humble-tf2-tools \
    ros-humble-tf-transformations \
    ros-humble-urdf-sim-tutorial \
    ros-humble-moveit \
    ros-humble-joint-trajectory-controller \
    ros-humble-joint-state-broadcaster \
    ros-humble-ros2controlcli \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    ros-humble-ros-gz-image \
    ros-humble-gz-ros2-control \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/* \
    && rosdep init \
    && rosdep update

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc 
RUN echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
RUN echo "export _colcon_cd_root=/opt/ros/humble/" >> ~/.bashrc
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc
RUN echo "export XDG_RUNTIME_DIR=/tmp/runtime-futa" >> ~/.bashrc

WORKDIR /ros2_ws/src/
RUN pip3 install git+https://github.com/tingelst/robotiq_modbus_controller.git --upgrade
RUN pip3 install pymodbus==3.0.2 pyserial==3.5

# Generate bash commands
WORKDIR /ros2_ws/
RUN echo "source /opt/ros/humble/setup.bash && colcon build --symlink-install --executor sequential && source /ros2_ws/install/setup.bash" >> ~/.bash_history
RUN echo "ros2 service call /hande/set_command hande_interfaces/srv/SetCommand \"{command: 'c'}\"" >> ~/.bash_history
RUN echo "ros2 service call /hande/set_command hande_interfaces/srv/SetCommand \"{command: 'o'}\"" >> ~/.bash_history
RUN echo "ros2 launch hande_tutorials server.launch.py is_real:=False" >> ~/.bash_history
RUN echo "ros2 launch hande_tutorials server.launch.py is_real:=True" >> ~/.bash_history
RUN echo "ros2 launch hande_tutorials demo.launch.py is_real:=False" >> ~/.bash_history
RUN echo "ros2 launch hande_tutorials demo.launch.py is_real:=True" >> ~/.bash_history
RUN echo "ros2 launch hande_description display.launch.py" >> ~/.bash_history
RUN echo "ros2 launch hande_control control.launch.py" >> ~/.bash_history
RUN echo "ros2 launch hande_gazebo gazebo.launch.py" >> ~/.bash_history
RUN echo "ros2 topic pub --once /hande_controller/commands std_msgs/msg/Float64MultiArray '{data: [0.0, 0.0]}'" >> ~/.bash_history
RUN echo "ros2 topic pub --once /hande_controller/commands std_msgs/msg/Float64MultiArray '{data: [2.5, 2.5]}'" >> ~/.bash_history
