#ifndef DLIO_PROFILER_CONFIG_HPP
#define DLIO_PROFILER_CONFIG_HPP

/* Version string for DLIO_PROFILER */
#define DLIO_PROFILER_PACKAGE_VERSION @DLIO_PROFILER_PACKAGE_VERSION @
#define DLIO_PROFILER_GIT_VERSION @DLIO_PROFILER_GIT_VERSION @

/* Compiler used */
#define CMAKE_BUILD_TYPE "Release"

#define CMAKE_C_COMPILER "/usr/lib64/ccache/cc"
#define CMAKE_C_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations"
#define CMAKE_C_FLAGS_DEBUG "-g"
#define CMAKE_C_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG"
#define CMAKE_C_FLAGS_RELEASE " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations_RELEASE"

#define CMAKE_CXX_COMPILER "/usr/lib64/ccache/c++"
#define CMAKE_CXX_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wnon-virtual-dtor -Wno-deprecated-declarations"
#define CMAKE_CXX_FLAGS_DEBUG "-g"
#define CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG"
#define CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG"

/* #undef CMAKE_C_SHARED_LIBRARY_FLAGS */
/* #undef CMAKE_CXX_SHARED_LIBRARY_FLAGS */

/* Macro flags */
/* #undef DLIO_PROFILER_GNU_LINUX */

//==========================
// Common macro definitions
//==========================

#define DLIO_PROFILER_PATH_DELIM "/"

// #define DLIO_PROFILER_NOOP_MACRO do {} while (0)
#define DLIO_PROFILER_NOOP_MACRO

// Detect VAR_OPT
// https://stackoverflow.com/questions/48045470/portably-detect-va-opt-support
#if __cplusplus <= 201703 && defined __GNUC__ && !defined __clang__ && \
    !defined __EDG__
#define VA_OPT_SUPPORTED false
#else
#define PP_THIRD_ARG(a, b, c, ...) c
#define VA_OPT_SUPPORTED_I(...) PP_THIRD_ARG(__VA_OPT__(, ), true, false, )
#define VA_OPT_SUPPORTED VA_OPT_SUPPORTED_I(?)
#endif

#if !defined(DLIO_PROFILER_HASH_SEED) || (DLIO_PROFILER_HASH_SEED <= 0)
#define DLIO_PROFILER_SEED 104723u
#endif

#endif /* DLIO_PROFILER_CONFIG_H */
