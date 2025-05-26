cmake_minimum_required(VERSION 3.5)
project(hande_description)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  urdf
)

catkin_package()

install(DIRECTORY
  urdf
  rviz
  meshes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)