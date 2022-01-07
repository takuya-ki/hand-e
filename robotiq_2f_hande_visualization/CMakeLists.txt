cmake_minimum_required(VERSION 3.5)
project(robotiq_2f_hande_visualization)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(urdf REQUIRED)

install(DIRECTORY meshes urdf rviz
  DESTINATION share/${PROJECT_NAME}
)