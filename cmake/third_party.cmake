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

# Third party libraries used by LaTeX2AI.

# The sources are only downloaded (SOURCE_SUBDIR points to a non-existing folder, so their
# own CMake projects are not added). The compiled sources are built directly into the
# plug-in, so they get the same compiler flags.
include(FetchContent)
set(_tpl_no_cmake SOURCE_SUBDIR "do_not_add_subdirectory")

# Third party sources that are compiled into the plug-in
set(TPL_SOURCES)
# Include roots of the third party headers (included as <...>)
set(TPL_INCLUDE_DIRS)

#
# nlohmann/json v3.10.4
#
FetchContent_Declare(json
  URL https://github.com/nlohmann/json/releases/download/v3.10.4/json.tar.xz
  URL_HASH SHA256=7af5ae79f61b0cb814fd6b121f3fe163cd09a8908295e8c98d8bbc1021bea8b3
  DOWNLOAD_EXTRACT_TIMESTAMP ON
  ${_tpl_no_cmake}
)
FetchContent_MakeAvailable(json)
list(APPEND TPL_INCLUDE_DIRS ${json_SOURCE_DIR}/single_include)

#
# cpp-semver (v0.3.3)
#
FetchContent_Declare(cpp_semver
  GIT_REPOSITORY https://github.com/z4kn4fein/cpp-semver.git
  GIT_TAG 620835768635a68b8fc68802992f9e59a9aa7993
  ${_tpl_no_cmake}
)
FetchContent_MakeAvailable(cpp_semver)
list(APPEND TPL_INCLUDE_DIRS ${cpp_semver_SOURCE_DIR}/include)

#
# CRCpp 1.2.0.0
#
FetchContent_Declare(crcpp
  GIT_REPOSITORY https://github.com/d-bahr/CRCpp.git
  GIT_TAG 85034fb49ad3e5490533313dd280441a3915a275
  ${_tpl_no_cmake}
)
FetchContent_MakeAvailable(crcpp)
list(APPEND TPL_INCLUDE_DIRS ${crcpp_SOURCE_DIR}/inc)

#
# tinyxml2 9.0.0
#
FetchContent_Declare(tinyxml2
  GIT_REPOSITORY https://github.com/leethomason/tinyxml2.git
  GIT_TAG 1dee28e51f9175a31955b9791c74c430fe13dc82
  ${_tpl_no_cmake}
)
FetchContent_MakeAvailable(tinyxml2)
list(APPEND TPL_INCLUDE_DIRS ${tinyxml2_SOURCE_DIR})
list(APPEND TPL_SOURCES ${tinyxml2_SOURCE_DIR}/tinyxml2.cpp)

#
# base64
#
FetchContent_Declare(base64
  GIT_REPOSITORY https://github.com/isteinbrecher/base64.git
  GIT_TAG 1a2e09a5342676e8c5eff629b3e43a4792d436e5
  ${_tpl_no_cmake}
)
FetchContent_MakeAvailable(base64)
list(APPEND TPL_INCLUDE_DIRS ${base64_SOURCE_DIR}/src)
list(APPEND TPL_SOURCES ${base64_SOURCE_DIR}/src/base64.cpp)

#
# StackWalker 1.20
#
if(WIN32)
  FetchContent_Declare(stackwalker
    GIT_REPOSITORY https://github.com/JochenKalmbach/StackWalker.git
    GIT_TAG 020706a2972bff842d8976ef81825f57e197eea5
    ${_tpl_no_cmake}
  )
  FetchContent_MakeAvailable(stackwalker)
  list(APPEND TPL_INCLUDE_DIRS ${stackwalker_SOURCE_DIR}/Main/StackWalker)
  set(STACKWALKER_SOURCE ${stackwalker_SOURCE_DIR}/Main/StackWalker/StackWalker.cpp)
  list(APPEND TPL_SOURCES ${STACKWALKER_SOURCE})
  # Disable some static analysis warnings
  set_source_files_properties(${STACKWALKER_SOURCE} PROPERTIES
    COMPILE_OPTIONS "/wd6340;/wd28159;/wd6011;/wd6388;/wd6387")
endif()
