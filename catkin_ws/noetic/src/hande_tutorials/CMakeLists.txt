cmake_minimum_required(VERSION 3.5)
project(hande_tutorials)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  urdf
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/demo_closeopen.py
  scripts/hande_service.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY
  urdf
  rviz
  meshes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)