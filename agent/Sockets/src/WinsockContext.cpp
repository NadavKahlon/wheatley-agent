#include <stdexcept>
#include <ws2tcpip.h>
#include <string>
#include <WinsockContext.hpp>

#pragma comment(lib, "Ws2_32.lib")

WinsockContext::WinsockContext()
{
    // TODO Maintain a static atomic counter so that we'll only need to do it once
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        throw std::runtime_error("WSAStartup failed: " + std::to_string(result));
    }
}

WinsockContext::~WinsockContext()
{
    WSACleanup();
}
