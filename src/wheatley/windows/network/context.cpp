#include <stdexcept>
#include <ws2tcpip.h>
#include <string>
#include <wheatley/common/network/context.hpp>

#pragma comment(lib, "Ws2_32.lib")

using namespace wheatley::network;
    
Context::Context()
{
    // TODO Maintain a static atomic counter so that we'll only need to do it once
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        throw std::runtime_error("WSAStartup failed: " + std::to_string(result));
    }
}

Context::~Context()
{
    WSACleanup();
}
