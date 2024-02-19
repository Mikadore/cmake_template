include(lib/CPM.cmake)
# Done as a function so that updates to variables like
# CMAKE_CXX_FLAGS don't propagate out to other
# targets
function(myproject_setup_dependencies)
	cpmaddpackage("gh:fmtlib/fmt#9.1.0")
	cpmaddpackage("gh:catchorg/Catch2@3.3.2")
	cpmaddpackage("gh:CLIUtils/CLI11@2.3.2")
	cpmaddpackage("gh:ArthurSonzogni/FTXUI@5.0.0")
	cpmaddpackage("gh:lefticus/tools#update_build_system")
	cpmaddpackage(
		NAME spdlog
		VERSION 1.11.0
		GITHUB_REPOSITORY "gabime/spdlog"
		OPTIONS "SPDLOG_FMT_EXTERNAL ON")

endfunction()