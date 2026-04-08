#ifdef _WIN32
#include <chell/windows/network/tcp_connection.hpp>
#elif defined(__linux__)
#include <chell/linux/network/tcp_connection.hpp>
#else
#error "Platform not supported"
#endif
