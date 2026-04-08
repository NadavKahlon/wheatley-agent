#ifdef _WIN32
#include <wheatley/windows/network/tcp_connection.hpp>
#elif defined(__linux__)
#include <wheatley/linux/network/tcp_connection.hpp>
#else
#error "Platform not supported"
#endif
