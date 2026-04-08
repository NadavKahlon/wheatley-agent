cmake_minimum_required(VERSION 3.10)

project(chell VERSION 0.1.0)


# Common sources
file(GLOB_RECURSE SOURCES 
    "src/chell/agent.cpp"
    "src/chell/main.cpp"
)

# Platform-specific sources
if(WIN32)
    file(GLOB_RECURSE PLATFORM_SOURCES 
        "src/chell/windows/network/context.cpp"
        "src/chell/windows/network/tcp_connection.cpp"
    )
elseif(UNIX AND NOT APPLE)
    file(GLOB_RECURSE PLATFORM_SOURCES 
        "src/chell/linux/network/context.cpp"
        "src/chell/linux/network/tcp_connection.cpp"
    )
endif()
list(APPEND SOURCES ${PLATFORM_SOURCES})

# Add target to compile `chell.exe` from sources
add_executable(${PROJECT_NAME} ${SOURCES})

# Enable `#include` from `src/` when compiling `chell.exe`
target_include_directories(${PROJECT_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/src)

# Link target against `aperture_protos` library
include(FetchContent)
FetchContent_Declare(
  aperture_protos
  GIT_REPOSITORY https://github.com/NadavKahlon/aperture-c2-protos.git
  GIT_TAG        dev
)
FetchContent_MakeAvailable(aperture_protos)
target_link_libraries(${PROJECT_NAME} PUBLIC aperture_protos)
target_include_directories(${PROJECT_NAME} PRIVATE 
    ${aperture_protos_SOURCE_DIR}
    ${aperture_protos_BINARY_DIR}
)
