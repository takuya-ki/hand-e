cmake_minimum_required(VERSION 3.5)
project(hande_interfaces)

find_package(catkin REQUIRED COMPONENTS
  message_generation
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SetCommand.srv
)

generate_messages(
  DEPENDENCIES
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)