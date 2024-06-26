-- LMod module file for BRAHMA

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
-- BRAHMA_GNU_LINUX: TRUE
-- BRAHMA_HAS_DOXYGEN: 
-- BRAHMA_HAS_STD_FILESYSTEM: TRUE
-- BRAHMA_HAS_STD_FSTREAM_FD: TRUE

help(
[[
Brahma (BRAHMA) version (0, 0, 5).
]])

whatis("Package: BRAHMA")
whatis("Version: (0, 0, 5)")
whatis("Description: DYnamic and Asynchronous Data streamliner (BRAHMA).")
whatis("URL: https://github.com/flux-framework/brahma")
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
whatis("BRAHMA_GNU_LINUX: TRUE")
whatis("BRAHMA_HAS_DOXYGEN: ")
whatis("BRAHMA_HAS_STD_FILESYSTEM: TRUE")
whatis("BRAHMA_HAS_STD_FSTREAM_FD: TRUE")

prepend_path("PATH","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/bin")
prepend_path("LD_LIBRARY_PATH","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/lib64")

pushenv("BRAHMA_DIR","/usr/WS2/haridev/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/")
