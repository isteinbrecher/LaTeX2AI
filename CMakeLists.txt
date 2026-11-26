# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2020-2026 Ivo Steinbrecher
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.21)

#
# Locate the Illustrator SDK
#
set(AI_SDK_DIR "" CACHE PATH "Path to the Adobe Illustrator SDK")
if(NOT AI_SDK_DIR)
  message(FATAL_ERROR
    "The path to the Adobe Illustrator SDK is not set. Configure with\n"
    "  cmake -DAI_SDK_DIR=<path to the SDK> ...\n"
    "The SDK folder contains 'illustratorapi' and 'samplecode'.")
endif()
get_filename_component(AI_SDK_DIR "${AI_SDK_DIR}" ABSOLUTE)
if(NOT EXISTS "${AI_SDK_DIR}/illustratorapi" OR NOT EXISTS "${AI_SDK_DIR}/samplecode/common")
  message(FATAL_ERROR
    "'${AI_SDK_DIR}' is not an Adobe Illustrator SDK.")
endif()
set(AI_COMMON "${AI_SDK_DIR}/samplecode/common")
set(AI_API "${AI_SDK_DIR}/illustratorapi")

#
# macOS settings
#
if(CMAKE_HOST_APPLE)
  # Default deployment target: the highest one the SDK's xcconfig requests for any architecture.
  if(NOT CMAKE_OSX_DEPLOYMENT_TARGET)
    set(_ai_deployment_target "12.0")
    file(STRINGS "${AI_COMMON}/mac/AIPluginCommon.xcconfig" _ai_deployment_lines
         REGEX "^MACOSX_DEPLOYMENT_TARGET")
    if(_ai_deployment_lines)
      set(_ai_deployment_target "0")
      foreach(_line IN LISTS _ai_deployment_lines)
        string(REGEX MATCH "[0-9]+(\\.[0-9]+)*[ \t]*$" _version "${_line}")
        string(STRIP "${_version}" _version)
        if(_version VERSION_GREATER _ai_deployment_target)
          set(_ai_deployment_target "${_version}")
        endif()
      endforeach()
    endif()
    set(CMAKE_OSX_DEPLOYMENT_TARGET "${_ai_deployment_target}" CACHE STRING "Minimum macOS version")
  endif()
endif()

#
# Multi-config generators (Xcode, Visual Studio): only offer Debug and Release
#
set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE)

#
# The plug-in version is taken from the source code
#
file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/src/l2a_constants.h" _l2a_version_line
     REGEX "#define L2A_VERSION_STRING_")
string(REGEX MATCH "[0-9]+\\.[0-9]+\\.[0-9]+" L2A_VERSION "${_l2a_version_line}")

#
# Define the project
#
if(CMAKE_HOST_APPLE)
  project(LaTeX2AI VERSION ${L2A_VERSION} LANGUAGES C CXX OBJCXX)
elseif(CMAKE_HOST_WIN32)
  # Static MSVC runtime (/MT, /MTd), as required for Illustrator plug-ins
  set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
  project(LaTeX2AI VERSION ${L2A_VERSION} LANGUAGES C CXX RC)
else()
  message(FATAL_ERROR "LaTeX2AI can only be built on macOS or Windows.")
endif()
message(STATUS "Using Illustrator SDK: ${AI_SDK_DIR}")

#
# Single-config generators (Ninja, Makefiles): default to Release
#
get_property(_is_multi_config GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)
if(NOT _is_multi_config AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type (Debug or Release)" FORCE)
endif()

#
# Locate python for the automatic generation of headers
#
find_package(Python3 REQUIRED COMPONENTS Interpreter)

#
# Define language options
#
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_OBJCXX_STANDARD 23)
set(CMAKE_OBJCXX_STANDARD_REQUIRED ON)
set(CMAKE_OBJCXX_EXTENSIONS OFF)

#
# Add source files via a macro
#
function(l2a_add_sources)
  file(GLOB _sources CONFIGURE_DEPENDS "${CMAKE_CURRENT_LIST_DIR}/*.cpp")
  file(GLOB _headers CONFIGURE_DEPENDS "${CMAKE_CURRENT_LIST_DIR}/*.h")
  set(L2A_SOURCES ${L2A_SOURCES} ${_sources} PARENT_SCOPE)
  set(L2A_HEADERS ${L2A_HEADERS} ${_headers} PARENT_SCOPE)
  set(L2A_INCLUDE_DIRS ${L2A_INCLUDE_DIRS} "${CMAKE_CURRENT_LIST_DIR}" PARENT_SCOPE)
endfunction()

set(L2A_SOURCES)
set(L2A_HEADERS)
set(L2A_INCLUDE_DIRS)
include(src/sources.cmake)

#
# Single-config generators (Ninja, Makefiles): default to Release
#
source_group(TREE "${CMAKE_CURRENT_SOURCE_DIR}/src" PREFIX "src" FILES ${L2A_SOURCES} ${L2A_HEADERS})

#
# Third party libraries
#
include(cmake/third_party.cmake)

#
# Add the sources that have to be compiled from the SDK
#
set(SDK_SOURCES
  ${AI_COMMON}/source/AppContext.cpp
  ${AI_COMMON}/source/HtmlUIController.cpp
  ${AI_COMMON}/source/IllustratorSDK.cpp
  ${AI_COMMON}/source/Main.cpp
  ${AI_COMMON}/source/Plugin.cpp
  ${AI_COMMON}/source/SDKAboutPluginsHelper.cpp
  ${AI_COMMON}/source/SDKPlugPlug.cpp
  ${AI_COMMON}/source/Suites.cpp
  ${AI_API}/illustrator/IAIFilePath.cpp
  ${AI_API}/illustrator/IAIStringFormatUtils.cpp
  ${AI_API}/illustrator/IAIUnicodeString.cpp
)

#
# Resources
#
set(L2A_SVG_RESOURCES
  resources/raw/LaTeX2AI_tool_create_dark@2x.svg
  resources/raw/LaTeX2AI_tool_create_light@2x.svg
  resources/raw/LaTeX2AI_tool_redo_dark@2x.svg
  resources/raw/LaTeX2AI_tool_redo_light@2x.svg
  resources/raw/LaTeX2AI_tool_options_dark@2x.svg
  resources/raw/LaTeX2AI_tool_options_light@2x.svg
  resources/raw/LaTeX2AI_tool_save_as_pdf_dark@2x.svg
  resources/raw/LaTeX2AI_tool_save_as_pdf_light@2x.svg
  resources/raw/LaTeX2AI_tool_testing_dark@2x.svg
  resources/raw/LaTeX2AI_tool_testing_light@2x.svg
  resources/raw/LaTeX2AI_cursor_create@2x.svg
  resources/raw/LaTeX2AI_cursor_locked@2x.svg
  resources/raw/LaTeX2AI_cursor_edit@2x.svg
)
set(L2A_TXT_RESOURCES resources/raw/IDToFile.txt)

#
# Generate the headers with the version and the LaTeX commands
#
add_custom_target(${PROJECT_NAME}_headers
  COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/scripts/create_headers.py"
  BYPRODUCTS
    "${CMAKE_CURRENT_SOURCE_DIR}/src/auto_generated/version.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/auto_generated/tex.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/ui/js/auto_generated.js"
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  COMMENT "Generating LaTeX2AI headers"
  VERBATIM
)

#
# PIPL
#
set(PIPL_INPUT "[{\"name\": \"${PROJECT_NAME}\", \"entry_point\": \"PluginMain\"}]")
set(PIPL_DIR "${CMAKE_CURRENT_BINARY_DIR}/pipl")
set(PIPL_FILE "${PIPL_DIR}/plugin.pipl")
file(MAKE_DIRECTORY "${PIPL_DIR}")
add_custom_command(
  OUTPUT "${PIPL_FILE}"
  COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/scripts/pipl/create_pipl.py"
          -input "${PIPL_INPUT}"
  WORKING_DIRECTORY "${PIPL_DIR}"
  DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt"
    "${CMAKE_CURRENT_SOURCE_DIR}/scripts/pipl/create_pipl.py"
    "${CMAKE_CURRENT_SOURCE_DIR}/scripts/pipl/pipl_gen/pipl_gen.py"
  COMMENT "Generating plugin.pipl"
  VERBATIM
)
add_custom_target(${PROJECT_NAME}_pipl DEPENDS "${PIPL_FILE}")

#
# Define how the aip file is created
#
add_library(${PROJECT_NAME} MODULE ${L2A_SOURCES} ${L2A_HEADERS} ${TPL_SOURCES} ${SDK_SOURCES})
add_dependencies(${PROJECT_NAME} ${PROJECT_NAME}_headers ${PROJECT_NAME}_pipl)

set_target_properties(${PROJECT_NAME} PROPERTIES
  PREFIX ""
  # Put the plug-in at <build>/<Config>/LaTeX2AI.aip for all generators
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>"
)

target_include_directories(${PROJECT_NAME} PRIVATE
  ${L2A_INCLUDE_DIRS}
  ${AI_COMMON}/includes
  ${AI_API}/ate
  ${AI_API}/illustrator
  ${AI_API}/illustrator/actions
  ${AI_API}/pica_sp
)
# Third party headers are system headers: included with <...> and their warnings are hidden
target_include_directories(${PROJECT_NAME} SYSTEM PRIVATE ${TPL_INCLUDE_DIRS})

target_compile_definitions(${PROJECT_NAME} PRIVATE
  $<$<CONFIG:Debug>:_DEBUG>
)

# Equivalent of the SDK's prefix header (IllustratorSDK{Debug,Release}.pch)
target_precompile_headers(${PROJECT_NAME} PRIVATE
  "${AI_COMMON}/includes/PluginStd.h"
  "${AI_COMMON}/includes/IllustratorSDK.h"
)

# Optional: copy the finished plug-in into a folder Illustrator loads plug-ins from
set(AI_PLUGIN_DEPLOY_DIR "" CACHE PATH "Folder the built plug-in is copied to after each build")

# Optional: set the path to the Illustrator executable for debugging in Xcode or Visual Studio.
set(AI_APP_PATH "" CACHE FILEPATH "Illustrator app launched by the IDE scheme")

if(APPLE)
  # The SDK compiles all C++ as Objective-C++ on macOS
  set_source_files_properties(${L2A_SOURCES} ${TPL_SOURCES} ${SDK_SOURCES} PROPERTIES LANGUAGE OBJCXX)

  set(MAC_RESOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/resources/Mac")
  set_target_properties(${PROJECT_NAME} PROPERTIES
    BUNDLE TRUE
    BUNDLE_EXTENSION "aip"
    MACOSX_BUNDLE_INFO_PLIST "${MAC_RESOURCE_DIR}/Info.plist.in"
    MACOSX_BUNDLE_BUNDLE_NAME "${PROJECT_NAME}"
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.adobe.illustrator.plugins.${PROJECT_NAME}"
    MACOSX_BUNDLE_BUNDLE_VERSION "${PROJECT_VERSION}"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "${PROJECT_VERSION}"
    CXX_VISIBILITY_PRESET hidden
    OBJCXX_VISIBILITY_PRESET hidden
  )
  target_compile_definitions(${PROJECT_NAME} PRIVATE $<$<CONFIG:Debug>:DEBUG=1>)
  target_link_libraries(${PROJECT_NAME} PRIVATE "-framework Cocoa")
  target_link_options(${PROJECT_NAME} PRIVATE $<$<CONFIG:Release>:-Wl,-dead_strip>)

  # Contents/Resources/LaTeX2AI.rsrc: Illustrator 2027 refuses a plug-in bundle without it,
  # even though it no longer reads resources from it. Our .r files only include Carbon.r, so
  # Rez on an empty input produces an identical (empty) resource map.
  find_program(REZ_EXECUTABLE Rez HINTS /Applications/Xcode.app/Contents/Developer/usr/bin REQUIRED)
  set(EMPTY_R_FILE "${CMAKE_CURRENT_BINARY_DIR}/empty.r")
  set(RSRC_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.rsrc")
  file(WRITE "${EMPTY_R_FILE}" "")
  add_custom_command(
    OUTPUT "${RSRC_FILE}"
    COMMAND "${REZ_EXECUTABLE}" -useDF -o "${RSRC_FILE}" "${EMPTY_R_FILE}"
    COMMENT "Generating ${PROJECT_NAME}.rsrc"
    VERBATIM
  )
  add_custom_target(${PROJECT_NAME}_rsrc DEPENDS "${RSRC_FILE}")
  add_dependencies(${PROJECT_NAME} ${PROJECT_NAME}_rsrc)

  # Contents/PkgInfo is required, otherwise macOS (and thus Illustrator) does not treat the
  # .aip directory as a package. Xcode generates it automatically, CMake does not.
  set(PKGINFO_FILE "${CMAKE_CURRENT_BINARY_DIR}/PkgInfo")
  file(WRITE "${PKGINFO_FILE}" "ARPIART5")

  # Post-build: copy all resources into the bundle, THEN sign it. Anything added after
  # signing breaks the signature seal and Illustrator refuses the plug-in.
  set(_bundle_resources "$<TARGET_BUNDLE_CONTENT_DIR:${PROJECT_NAME}>/Resources")
  add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory "${_bundle_resources}/pipl" "${_bundle_resources}/svg" "${_bundle_resources}/txt"
    COMMAND ${CMAKE_COMMAND} -E copy "${PIPL_FILE}" "${_bundle_resources}/pipl/plugin.pipl"
    COMMAND ${CMAKE_COMMAND} -E copy ${L2A_SVG_RESOURCES} "${_bundle_resources}/svg/"
    COMMAND ${CMAKE_COMMAND} -E copy ${L2A_TXT_RESOURCES} "${_bundle_resources}/txt/"
    COMMAND ${CMAKE_COMMAND} -E copy "${RSRC_FILE}" "${_bundle_resources}/${PROJECT_NAME}.rsrc"
    COMMAND ${CMAKE_COMMAND} -E copy "${PKGINFO_FILE}" "$<TARGET_BUNDLE_CONTENT_DIR:${PROJECT_NAME}>/PkgInfo"
    COMMAND codesign --force --sign - "$<TARGET_BUNDLE_DIR:${PROJECT_NAME}>"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    COMMENT "Adding resources and signing ${PROJECT_NAME}.aip"
    VERBATIM
  )

  if(AI_PLUGIN_DEPLOY_DIR)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E rm -rf "${AI_PLUGIN_DEPLOY_DIR}/${PROJECT_NAME}.aip"
      COMMAND ${CMAKE_COMMAND} -E copy_directory "$<TARGET_BUNDLE_DIR:${PROJECT_NAME}>" "${AI_PLUGIN_DEPLOY_DIR}/${PROJECT_NAME}.aip"
      COMMENT "Deploying ${PROJECT_NAME}.aip to ${AI_PLUGIN_DEPLOY_DIR}"
      VERBATIM
    )
  endif()

  # Xcode: Run/Debug launches Illustrator with the debugger attached
  set_target_properties(${PROJECT_NAME} PROPERTIES
    XCODE_GENERATE_SCHEME ON
    XCODE_SCHEME_EXECUTABLE "${AI_APP_PATH}"
  )

elseif(WIN32)
  set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".aip")

  # Resources (PiPL, SVG icons, IDToFile.txt) are compiled into the DLL
  set(WIN_RC_FILE resources/Win/LaTeX2AI.rc)
  target_sources(${PROJECT_NAME} PRIVATE
    ${WIN_RC_FILE}
    ${AI_COMMON}/win/PluginMain.def
  )
  set_source_files_properties(${WIN_RC_FILE} PROPERTIES
    OBJECT_DEPENDS "${PIPL_FILE};${CMAKE_CURRENT_SOURCE_DIR}/resources/raw/IDToFile.txt")
  target_include_directories(${PROJECT_NAME} PRIVATE
    resources/raw
    ${AI_COMMON}/win
    ${PIPL_DIR}
  )

  target_compile_definitions(${PROJECT_NAME} PRIVATE
    WIN_ENV
    NOMINMAX
    $<$<CONFIG:Release>:_WINDOWS>
  )
  set(_msvc_options
    /W4          # Warning level 4
    /Zp8         # Struct member alignment 8 bytes (as the SDK expects)
    /Zc:wchar_t- # wchar_t is not a built-in type (as the SDK expects)
    /GF          # String pooling
    /Gy          # Function level linking
    /FIpragma.h  # SDK pragmas, forced include
  )
  if(CMAKE_GENERATOR MATCHES "Visual Studio")
    list(APPEND _msvc_options /MP)
  endif()
  target_compile_options(${PROJECT_NAME} PRIVATE "$<$<COMPILE_LANGUAGE:C,CXX>:${_msvc_options}>")
  target_link_options(${PROJECT_NAME} PRIVATE /DYNAMICBASE:NO /LARGEADDRESSAWARE /SUBSYSTEM:WINDOWS)

  # These files do not use the precompiled header
  set_source_files_properties(
    ${TPL_SOURCES}
    ${AI_COMMON}/source/SDKPlugPlug.cpp
    ${AI_API}/illustrator/IAIFilePath.cpp
    PROPERTIES SKIP_PRECOMPILE_HEADERS ON
  )
  set_source_files_properties(${AI_COMMON}/source/Plugin.cpp PROPERTIES COMPILE_OPTIONS "/wd4100")

  if(AI_PLUGIN_DEPLOY_DIR)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy "$<TARGET_FILE:${PROJECT_NAME}>" "${AI_PLUGIN_DEPLOY_DIR}/${PROJECT_NAME}.aip"
      COMMENT "Deploying ${PROJECT_NAME}.aip to ${AI_PLUGIN_DEPLOY_DIR}"
      VERBATIM
    )
  endif()

  # Visual Studio: Run/Debug launches Illustrator with the debugger attached
  set_target_properties(${PROJECT_NAME} PROPERTIES VS_DEBUGGER_COMMAND "${AI_APP_PATH}")
  set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT ${PROJECT_NAME})
endif()
