cmake_minimum_required(VERSION 3.28)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)


# Set the project name and language
project(
	myproject
	VERSION 0.0.1
	DESCRIPTION ""
	LANGUAGES CXX C
)

add_library(myproject_options INTERFACE)
add_library(myproject_warnings INTERFACE)
add_library(myproject::myproject_options ALIAS myproject_options)
add_library(myproject::myproject_warnings ALIAS myproject_warnings)

include(CMakeDependentOption)
include(CheckCXXCompilerFlag)
include(cmake/Dependencies.cmake)
include(cmake/lib/SystemLink.cmake)
include(cmake/lib/StandardProjectSettings.cmake)
include(cmake/lib/CompilerWarnings.cmake)
include(cmake/lib/Linker.cmake)
include(cmake/lib/Harden.cmake)
include(cmake/lib/Sanitizers.cmake)
include(cmake/lib/StaticAnalyzers.cmake)

#include(cmake/lib/Tests.cmake)
#myproject_enable_coverage(myproject_options)
# don't know if this should be set globally from here or not...
target_compile_features(myproject_options INTERFACE cxx_std_${CMAKE_CXX_STANDARD})

add_subdirectory(bin)
add_subdirectory(lib)
add_subdirectory(tests)