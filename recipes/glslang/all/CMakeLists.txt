cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
else()
  include(conanbuildinfo.cmake)
endif()
conan_basic_setup(TARGETS)

# The orignal CMakeLists.txt provided by glslang is very awkward
# You must manually check out the SPIRV-Tools in the glslang/External
# folder and then the cmake adds it as add_subdirectory
# It then check sif the SPIRV-Tools-opt target was built and if it was
# only then it will enable SPIRV optimization.
#
# Since we are building spirv-tools as a separate conan package
# the SPIRV-Tools-opt target will not exist, so we have to manually create
# it as an interface target so that when glslang builds, it will find
# the library.
add_library( SPIRV-Tools-opt INTERFACE)
target_link_libraries( SPIRV-Tools-opt INTERFACE CONAN_PKG::spirv-tools)

# Export the target because it's complaining
install(TARGETS SPIRV-Tools-opt EXPORT SPIRVTargets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

add_subdirectory("source_subfolder")
