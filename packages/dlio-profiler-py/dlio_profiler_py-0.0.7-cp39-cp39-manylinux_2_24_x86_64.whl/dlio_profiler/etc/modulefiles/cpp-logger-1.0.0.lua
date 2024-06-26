-- LMod module file for CPP_LOGGER

-- CMAKE_INSTALL_PREFIX: /usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler
-- CMAKE_BUILD_TYPE: Release
-- C Compiler: /usr/lib64/ccache/cc
-- C FLAGS:  -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations
-- C FLAGS_DEBUG: -g
-- C FLAGS_RELWITHDEBINFO: -O2 -g -DNDEBUG
-- C FLAGS_RELEASE: -O3 -DNDEBUG
-- CXX Compiler: /usr/lib64/ccache/c++
-- CXX FLAGS:  -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wnon-virtual-dtor -Wno-deprecated-declarations
-- CXX FLAGS_DEBUG: -g
-- CXX FLAGS_RELWITHDEBINFO: -O2 -g -DNDEBUG
-- CXX FLAGS_RELEASE: -O3 -DNDEBUG
-- CPP_LOGGER_GNU_LINUX: TRUE
-- CPP_LOGGER_HAS_DOXYGEN: 

help(
[[
CPP Logger (CPP_LOGGER) version (0, 0, 4).
]])

whatis("Package: CPP_LOGGER")
whatis("Version: (0, 0, 4)")
whatis("Description: DYnamic and Asynchronous Data streamliner (CPP_LOGGER).")
whatis("URL: https://github.com/flux-framework/cpp_logger")
whatis("CMAKE_INSTALL_PREFIX: /usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler")
whatis("CMAKE_BUILD_TYPE: Release")
whatis("C Compiler: /usr/lib64/ccache/cc")
whatis("C FLAGS:  -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations")
whatis("C FLAGS_DEBUG: -g")
whatis("C FLAGS_RELWITHDEBINFO: -O2 -g -DNDEBUG")
whatis("C FLAGS_RELEASE: -O3 -DNDEBUG")
whatis("CXX Compiler: /usr/lib64/ccache/c++")
whatis("CXX FLAGS:  -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wnon-virtual-dtor -Wno-deprecated-declarations")
whatis("CXX FLAGS_DEBUG: -g")
whatis("CXX FLAGS_RELWITHDEBINFO: -O2 -g -DNDEBUG")
whatis("CXX FLAGS_RELEASE: -O3 -DNDEBUG")
whatis("CPP_LOGGER_GNU_LINUX: TRUE")
whatis("CPP_LOGGER_HAS_DOXYGEN: ")

prepend_path("PATH","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/bin")
prepend_path("LD_LIBRARY_PATH","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/lib64")

pushenv("CPP_LOGGER_DIR","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/")
