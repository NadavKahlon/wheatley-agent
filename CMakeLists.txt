cmake_minimum_required(VERSION 3.10)

project(wheatley VERSION 0.1.0)


# Common sources
set(SOURCES
    src/wheatley/common/main.cpp
    src/wheatley/common/network/tcp_connection.cpp
    src/wheatley/common/agent.cpp
)

# Platform-specific sources
if(WIN32)
    list(APPEND SOURCES 
        src/wheatley/windows/network_context.cpp
    )
elseif(UNIX AND NOT APPLE)
    list(APPEND SOURCES 
        src/wheatley/linux/network_context.cpp
    )
endif()

# Add target to compile `wheatley.exe` from sources
add_executable(${PROJECT_NAME} ${SOURCES})

# Enable `#include` from `src/` when compiling `wheatley.exe`
target_include_directories(${PROJECT_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/src)

# Link target against `wheatley_protos` library
include(FetchContent)
FetchContent_Declare(
  wheatley_protos
  GIT_REPOSITORY https://github.com/NadavKahlon/wheatley-protos.git
  GIT_TAG        c836a69
)
FetchContent_MakeAvailable(wheatley_protos)
target_link_libraries(${PROJECT_NAME} PUBLIC wheatley_protos)
target_include_directories(${PROJECT_NAME} PRIVATE 
    ${wheatley_protos_SOURCE_DIR}
    ${wheatley_protos_BINARY_DIR}
)
