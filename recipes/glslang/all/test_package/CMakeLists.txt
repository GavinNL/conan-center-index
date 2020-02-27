# This test package is the same as glslang/StandAlone/StandAlone.cpp that
# is included in the source tree.
# The StandAlone is the code for glslangValidator, which is the main application
# used to compile glsl->spirv.
#
# I wanted to use this as the test package to ensure that the compiled application
# produces proper SPIRV code.

cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} test_package.cpp ResourceLimits.cpp)

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
target_compile_definitions(${PROJECT_NAME}
                                PRIVATE
                                    CMAKE_CURRENT_SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}"
                                    ENABLE_OPT)


add_executable(${PROJECT_NAME}.2 test_package.2.cpp )

target_link_libraries(${PROJECT_NAME}.2 ${CONAN_LIBS})
target_compile_definitions(${PROJECT_NAME}.2
                                PRIVATE
                                    CMAKE_CURRENT_SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}")
