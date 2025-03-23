cmake_minimum_required(VERSION 3.10)
project(Project_SO2)

set(CMAKE_CXX_STANDARD 23)

add_executable(Project_SO2
        main.cpp
        ../SO2/classes/philosopher/philosopher.cpp
)