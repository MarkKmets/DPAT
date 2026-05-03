cmake_minimum_required(VERSION 3.10)
project(OpenCV_Modular_App)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
include_directories(include ${OpenCV_INCLUDE_DIRS})

file(GLOB SOURCES "src/*.cpp")

add_executable(opencv_app ${SOURCES})
target_link_libraries(opencv_app ${OpenCV_LIBS})
