cmake_minimum_required(VERSION 3.12)
project(entropy2d)

set(CMAKE_CXX_STANDARD 11)

# 必须要找到OpenCV库，否则无法运行
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_DIRS})

add_executable(entropy2d main.cpp)
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})