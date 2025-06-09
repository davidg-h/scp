cmake_minimum_required(VERSION 3.14)
project(sonycam)

# Enable C++14
set(CMAKE_CXX_STANDARD 14)

# Use pybind11 from GitHub via FetchContent (no pip needed)
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# Build Python module
pybind11_add_module(sonycam bindings.cpp DummySrc.cpp)
