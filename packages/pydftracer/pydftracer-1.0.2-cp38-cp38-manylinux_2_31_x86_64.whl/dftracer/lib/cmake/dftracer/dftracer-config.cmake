# This will create IMPORTED targets for DFTRACER. The executables will be
# DFTRACER::<exe-name>-bin (e.g., DFTRACER::dftracer-bin) and the library will
# be DFTRACER::dftracer.

include("${CMAKE_CURRENT_LIST_DIR}/DFTRACERConfigVersion.cmake")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/modules")
list(APPEND CMAKE_MODULE_PATH "")

#include(GNUInstallDirs)
include(ExternalProject)
include(DFTRACERCMakeUtilities)
include(CMakePackageConfigHelpers)


set(DFTRACER_VERSION ${PACKAGE_VERSION})

# Record compiler information
set(DFTRACER_C_COMPILER "/usr/bin/cc")
set(DFTRACER_CXX_COMPILER "/usr/bin/c++")

set(DFTRACER_C_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations")
set(DFTRACER_CXX_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wnon-virtual-dtor -Wno-deprecated-declarations")

set(DFTRACER_C_STANDARD "11")
set(DFTRACER_CXX_STANDARD "17")

set(CMAKE_C_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Record the various flags and switches accumlated in DFTRACER
set(DFTRACER_GNU_LINUX )
set(DFTRACER_HAS_STD_FILESYSTEM TRUE)
set(DFTRACER_HAS_STD_FSTREAM_FD TRUE)

# Setup dependencies




# Now actually import the DFTRACER target
set(_TMP_INCLUDE_DIRS "")
foreach (_DIR ${_TMP_INCLUDE_DIRS})
  set_and_check(_INCLUDE_DIR "${_DIR}")
  list(APPEND DFTRACER_INCLUDE_DIRS "${_INCLUDE_DIR}")
endforeach (_DIR "${_TMP_INCLUDE_DIRS}")

set(_TMP_LIBRARY_DIRS "")
foreach (_DIR ${_TMP_LIBRARY_DIRS})
  set_and_check(_LIBRARY_DIR "${_DIR}")
  list(APPEND DFTRACER_LIBRARY_DIRS "${_LIBRARY_DIR}")
endforeach (_DIR ${_TMP_LIBRARY_DIRS})

if (NOT TARGET DFTRACER::dftracer)
  include(${CMAKE_CURRENT_LIST_DIR}/DFTRACERTargets.cmake)
endif (NOT TARGET DFTRACER::dftracer)

check_required_components(DFTRACER)

set(DFTRACER_LIBRARIES DFTRACER::dftracer)
