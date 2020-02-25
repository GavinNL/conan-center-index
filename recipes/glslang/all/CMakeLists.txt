cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads)


get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()

#===============================================================================
# OSDependent
#===============================================================================
if(WIN32)
    set(OSDependent_SOURCES "source_subfolder/glslang/OSDependent/Windows/ossource.cpp" )
elseif(UNIX)
    set(OSDependent_SOURCES "source_subfolder/glslang/OSDependent/Unix/ossource.cpp" )
else(WIN32)
    message("unknown platform")
endif(WIN32)

add_library(OSDependent
              STATIC ${OSDependent_SOURCES})
set_property(TARGET OSDependent PROPERTY FOLDER glslang)
set_property(TARGET OSDependent PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(OSDependent PUBLIC Threads::Threads)

install(TARGETS OSDependent
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
#===============================================================================


#===============================================================================
# OSDependent
#===============================================================================
set(oglcompiler_SOURCES
    source_subfolder/OGLCompilersDLL/InitializeDll.cpp
  )

set(oglcompiler_HEADERS
    source_subfolder/OGLCompilersDLL/InitializeDll.h
    )

add_library(OGLCompiler
              ${oglcompiler_SOURCES})
set_property(TARGET OGLCompiler PROPERTY FOLDER glslang)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)
install(TARGETS OGLCompiler
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
#===============================================================================


#===============================================================================
# OSDependent
#===============================================================================
set(glslang_SOURCES
    source_subfolder/glslang/MachineIndependent/glslang.y
    source_subfolder/glslang/MachineIndependent/glslang_tab.cpp
    source_subfolder/glslang/MachineIndependent/attribute.cpp
    source_subfolder/glslang/MachineIndependent/Constant.cpp
    source_subfolder/glslang/MachineIndependent/iomapper.cpp
    source_subfolder/glslang/MachineIndependent/InfoSink.cpp
    source_subfolder/glslang/MachineIndependent/Initialize.cpp
    source_subfolder/glslang/MachineIndependent/IntermTraverse.cpp
    source_subfolder/glslang/MachineIndependent/Intermediate.cpp
    source_subfolder/glslang/MachineIndependent/ParseContextBase.cpp
    source_subfolder/glslang/MachineIndependent/ParseHelper.cpp
    source_subfolder/glslang/MachineIndependent/PoolAlloc.cpp
    source_subfolder/glslang/MachineIndependent/RemoveTree.cpp
    source_subfolder/glslang/MachineIndependent/Scan.cpp
    source_subfolder/glslang/MachineIndependent/ShaderLang.cpp
    source_subfolder/glslang/MachineIndependent/SymbolTable.cpp
    source_subfolder/glslang/MachineIndependent/Versions.cpp
    source_subfolder/glslang/MachineIndependent/intermOut.cpp
    source_subfolder/glslang/MachineIndependent/limits.cpp
    source_subfolder/glslang/MachineIndependent/linkValidate.cpp
    source_subfolder/glslang/MachineIndependent/parseConst.cpp
    source_subfolder/glslang/MachineIndependent/reflection.cpp
    source_subfolder/glslang/MachineIndependent/preprocessor/Pp.cpp
    source_subfolder/glslang/MachineIndependent/preprocessor/PpAtom.cpp
    source_subfolder/glslang/MachineIndependent/preprocessor/PpContext.cpp
    source_subfolder/glslang/MachineIndependent/preprocessor/PpScanner.cpp
    source_subfolder/glslang/MachineIndependent/preprocessor/PpTokens.cpp
    source_subfolder/glslang/MachineIndependent/propagateNoContraction.cpp
    source_subfolder/glslang/GenericCodeGen/CodeGen.cpp
  source_subfolder/glslang/GenericCodeGen/Link.cpp)

set(glslang_HEADERS
    source_subfolder/glslang/Public/ShaderLang.h
    source_subfolder/glslang/Include/arrays.h
    source_subfolder/glslang/Include/BaseTypes.h
    source_subfolder/glslang/Include/Common.h
    source_subfolder/glslang/Include/ConstantUnion.h
    source_subfolder/glslang/Include/InfoSink.h
    source_subfolder/glslang/Include/InitializeGlobals.h
    source_subfolder/glslang/Include/intermediate.h
    source_subfolder/glslang/Include/PoolAlloc.h
    source_subfolder/glslang/Include/ResourceLimits.h
    source_subfolder/glslang/Include/revision.h
    source_subfolder/glslang/Include/ShHandle.h
    source_subfolder/glslang/Include/Types.h
    source_subfolder/glslang/MachineIndependent/attribute.h
    source_subfolder/glslang/MachineIndependent/glslang_tab.cpp.h
    source_subfolder/glslang/MachineIndependent/gl_types.h
    source_subfolder/glslang/MachineIndependent/Initialize.h
    source_subfolder/glslang/MachineIndependent/iomapper.h
    source_subfolder/glslang/MachineIndependent/LiveTraverser.h
    source_subfolder/glslang/MachineIndependent/localintermediate.h
    source_subfolder/glslang/MachineIndependent/ParseHelper.h
    source_subfolder/glslang/MachineIndependent/reflection.h
    source_subfolder/glslang/MachineIndependent/RemoveTree.h
    source_subfolder/glslang/MachineIndependent/Scan.h
    source_subfolder/glslang/MachineIndependent/ScanContext.h
    source_subfolder/glslang/MachineIndependent/SymbolTable.h
    source_subfolder/glslang/MachineIndependent/Versions.h
    source_subfolder/glslang/MachineIndependent/parseVersions.h
    source_subfolder/glslang/MachineIndependent/propagateNoContraction.h
    source_subfolder/glslang/MachineIndependent/preprocessor/PpContext.h
    source_subfolder/glslang/MachineIndependent/preprocessor/PpTokens.h)

add_library(glslang
              ${glslang_SOURCES})
set_property(TARGET glslang PROPERTY FOLDER glslang)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(glslang OGLCompiler OSDependent)
target_include_directories(glslang PUBLIC ..)

install(TARGETS glslang
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})


#Copied from originan CMakeLists.txt
install(FILES
          source_subfolder/glslang/Include/arrays.h
          source_subfolder/glslang/Include/BaseTypes.h
          source_subfolder/glslang/Include/Common.h
          source_subfolder/glslang/Include/ConstantUnion.h
          source_subfolder/glslang/Include/InfoSink.h
          source_subfolder/glslang/Include/InitializeGlobals.h
          source_subfolder/glslang/Include/intermediate.h
          source_subfolder/glslang/Include/PoolAlloc.h
          source_subfolder/glslang/Include/ResourceLimits.h
          source_subfolder/glslang/Include/revision.h
          source_subfolder/glslang/Include/ShHandle.h
          source_subfolder/glslang/Include/Types.h
        DESTINATION
          ${CMAKE_INSTALL_INCLUDEDIR}/glslang/Include)


install(FILES
  source_subfolder/glslang/Public/ShaderLang.h
        DESTINATION
      ${CMAKE_INSTALL_INCLUDEDIR}/glslang/Public)

install(FILES
          source_subfolder/glslang/MachineIndependent/attribute.h
          source_subfolder/glslang/MachineIndependent/glslang_tab.cpp.h
          source_subfolder/glslang/MachineIndependent/gl_types.h
          source_subfolder/glslang/MachineIndependent/Initialize.h
          source_subfolder/glslang/MachineIndependent/iomapper.h
          source_subfolder/glslang/MachineIndependent/LiveTraverser.h
          source_subfolder/glslang/MachineIndependent/localintermediate.h
          source_subfolder/glslang/MachineIndependent/ParseHelper.h
          source_subfolder/glslang/MachineIndependent/reflection.h
          source_subfolder/glslang/MachineIndependent/RemoveTree.h
          source_subfolder/glslang/MachineIndependent/Scan.h
          source_subfolder/glslang/MachineIndependent/ScanContext.h
          source_subfolder/glslang/MachineIndependent/SymbolTable.h
          source_subfolder/glslang/MachineIndependent/Versions.h
          source_subfolder/glslang/MachineIndependent/parseVersions.h
          source_subfolder/glslang/MachineIndependent/propagateNoContraction.h
        DESTINATION
          ${CMAKE_INSTALL_INCLUDEDIR}/glslang/MachineIndependent)

install(FILES
          source_subfolder/glslang/MachineIndependent/preprocessor/PpContext.h
          source_subfolder/glslang/MachineIndependent/preprocessor/PpTokens.h
        DESTINATION
          ${CMAKE_INSTALL_INCLUDEDIR}/glslang/MachineIndependent/preprocessor)

#===============================================================================




#===============================================================================
# OSDependent
#===============================================================================
set(hlsl_SOURCES
    source_subfolder/hlsl/hlslAttributes.cpp
    source_subfolder/hlsl/hlslParseHelper.cpp
    source_subfolder/hlsl/hlslScanContext.cpp
    source_subfolder/hlsl/hlslOpMap.cpp
    source_subfolder/hlsl/hlslTokenStream.cpp
    source_subfolder/hlsl/hlslGrammar.cpp
  source_subfolder/hlsl/hlslParseables.cpp)

set(hlsl_HEADERS
  source_subfolders/hlsl/hlslAttributes.h
  source_subfolders/hlsl/hlslParseHelper.h
  source_subfolders/hlsl/hlslTokens.h
  source_subfolders/hlsl/hlslScanContext.h
  source_subfolders/hlsl/hlslOpMap.h
  source_subfolders/hlsl/hlslTokenStream.h
  source_subfolders/hlsl/hlslGrammar.h
  source_subfolders/hlsl/hlslParseables.h)

add_library(HLSL ${hlsl_SOURCES})
set_property(TARGET HLSL PROPERTY FOLDER glslang)

target_compile_definitions(HLSL PUBLIC ENABLE_HLSL)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)
install(TARGETS HLSL
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
#===============================================================================





#===============================================================================
# OSDependent
#===============================================================================
set(spirv_SOURCES
  source_subfolder/SPIRV/GlslangToSpv.cpp
  source_subfolder/SPIRV/InReadableOrder.cpp
  source_subfolder/SPIRV/Logger.cpp
  source_subfolder/SPIRV/SpvBuilder.cpp
  source_subfolder/SPIRV/SpvPostProcess.cpp
  source_subfolder/SPIRV/doc.cpp
  source_subfolder/SPIRV/SpvTools.cpp
  source_subfolder/SPIRV/disassemble.cpp)

set(spirv_HEADERS
   source_subfolder/SPIRV/bitutils.h
   source_subfolder/SPIRV/spirv.hpp
   source_subfolder/SPIRV/GLSL.std.450.h
   source_subfolder/SPIRV/GLSL.ext.EXT.h
   source_subfolder/SPIRV/GLSL.ext.KHR.h
   source_subfolder/SPIRV/GlslangToSpv.h
   source_subfolder/SPIRV/hex_float.h
   source_subfolder/SPIRV/Logger.h
   source_subfolder/SPIRV/SpvBuilder.h
   source_subfolder/SPIRV/spvIR.h
   source_subfolder/SPIRV/doc.h
   source_subfolder/SPIRV/SpvTools.h
   source_subfolder/SPIRV/disassemble.h)

add_library(SPIRV ${spirv_SOURCES})
set_property(TARGET SPIRV PROPERTY FOLDER glslang)
target_link_libraries(SPIRV PUBLIC SPIRV-Tools-opt)

target_link_libraries(SPIRV glslang SPIRV-Tools-opt)

install(TARGETS SPIRV
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

install(FILES ${spirv_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/SPIRV/)
install(FILES ${spirv_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glslang/SPIRV/)
#target_compile_definitions(HLSL PUBLIC ENABLE_HLSL)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)

#===============================================================================










#===============================================================================
# SPVRemapper
#===============================================================================
set(SOURCES
  source_subfolder/SPIRV/SPVRemapper.cpp
  source_subfolder/SPIRV/doc.cpp
)

set(HEADERS
   source_subfolder/SPIRV/SPVRemapper.h
   source_subfolder/SPIRV/doc.h
)

add_library(SPVRemapper ${SOURCES})
set_property(TARGET SPVRemapper PROPERTY FOLDER glslang)


install(TARGETS SPVRemapper
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
#target_compile_definitions(HLSL PUBLIC ENABLE_HLSL)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)
install(FILES ${HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/SPIRV/)
install(FILES ${HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glslang/SPIRV/)
#===============================================================================







#===============================================================================
#   source_subfolder/StandAlone/doc.cpp
#===============================================================================
set(SOURCES
  source_subfolder/StandAlone/ResourceLimits.cpp
)

#set(HEADERS
#   source_subfolder/SPIRV/SPVRemapper.h
#   source_subfolder/SPIRV/doc.hpp
#)

add_library(glslang-default-resource-limits ${SOURCES})
set_property(TARGET glslang-default-resource-limits PROPERTY FOLDER glslang)


install(TARGETS glslang-default-resource-limits
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

#target_compile_definitions(HLSL PUBLIC ENABLE_HLSL)
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)

#===============================================================================




#===============================================================================
#   source_subfolder/StandAlone/doc.cpp
#===============================================================================
set(SOURCES
  source_subfolder/StandAlone/StandAlone.cpp
  source_subfolder/StandAlone/DirStackFileIncluder.h
)

#set(HEADERS
#   source_subfolder/SPIRV/SPVRemapper.h
#   source_subfolder/SPIRV/doc.hpp
#)

add_executable(glslangValidator ${SOURCES})
set_property(TARGET glslangValidator PROPERTY FOLDER tools)

target_link_libraries(glslangValidator glslang SPIRV SPVRemapper glslang-default-resource-limits)
install(TARGETS glslangValidator
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

target_compile_definitions(glslangValidator PRIVATE "ENABLE_OPT=1")
#set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)

#target_link_libraries(glslang OGLCompiler OSDependent)
#target_include_directories(glslang PUBLIC ..)

#target_link_libraries(OSDependent Threads::Threads)

#===============================================================================

#add_library( SPIRV-Tools-opt INTERFACE )
#
#target_link_libraries( SPIRV-Tools-opt
#                          INTERFACE
#                          ${CONAN_LIBS})
#
#
#target_include_directories( SPIRV-Tools-opt
#                          INTERFACE
#                          ${CONAN_INCLUDE_DIRS})
#
#install(TARGETS SPIRV-Tools-opt OPTIONAL)
#
#target_compile_features( ${libName}
#                          INTERFACE
#                              cxx_std_17)
#
#target_compile_definitions( ${libName}
#                                INTERFACE
#                                TEST_DEFINE)
#
#target_link_libraries( ${libName}  INTERFACE  ${PublicLinkedTargets}  )
#target_link_libraries( ${libName}  INTERFACE ${PrivateLinkedTargets} )




#add_subdirectory("source_subfolder")
