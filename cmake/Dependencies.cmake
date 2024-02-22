include(cmake/lib/CPM.cmake)
# Done as a function so that updates to variables like
# CMAKE_CXX_FLAGS don't propagate out to other
# targets
	cpmaddpackage("gh:fmtlib/fmt#9.1.0")
	cpmaddpackage("gh:catchorg/Catch2@3.3.2")