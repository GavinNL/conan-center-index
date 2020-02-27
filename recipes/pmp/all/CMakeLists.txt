cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
else()
  include(conanbuildinfo.cmake)
endif()
conan_basic_setup()

################################################################################
# This CmakeLists.txt file was taken from the
# project's src/pmp/CMakeLists.txt file
#
# The original project's compiles a visualization library which depends on
# GLFW/Glad/OpenGL which is not currently provided by
# conan-center-index
#
# The original project's CMakeLists file does not :
#   - use find_package for external depenendices
#   - allow for enabling/disabling the different components (core, visualiation,
#     tools,etc )
#
# This made it difficult to use the original file to build the library.
# This list file only compiles the core/algorithm backend of the PMP
# library.
################################################################################

file(GLOB SOURCES source_subfolder/src/pmp/*.cpp)
file(GLOB HEADERS source_subfolder/src/pmp/*.h)

add_library(pmp ${SOURCES} ${HEADERS})
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS 1)

# This library depends on rply. The original lists file
# compiles this as a separate library.
# The rply library consists of static C functions
# so conflicts shouldn't arise if we compile the entier thing as a single
# library. rply headers are not needed to use PMP
target_sources(pmp PRIVATE source_subfolder/external/rply/rply.c)
target_include_directories(pmp PRIVATE source_subfolder/external/rply)

if(NOT (UNIX AND ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")))
  find_package(OpenMP)
  if(OPENMP_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    if(UNIX OR APPLE)
      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -msse")
    endif()
    if(MSVC)
      add_definitions(/arch:SSE)
    endif(MSVC)
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS_INIT} -fopenmp")
  endif()
endif()

set_target_properties(pmp PROPERTIES VERSION 1.1.0)

target_include_directories(pmp PUBLIC
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/src>
$<INSTALL_INTERFACE:include/>)

target_compile_features(pmp PRIVATE cxx_std_11)

install(TARGETS pmp EXPORT pmpTargets
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include)

  install(FILES ${HEADERS} DESTINATION include/pmp/)
