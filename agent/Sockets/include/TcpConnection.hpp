#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <winsock.h>
#include <memory>
#include <WinsockContext.hpp>

class TcpConnection {
public:
    TcpConnection(const std::string& ip, int port);
    ~TcpConnection();

    // Disable copying for RAII integrity
    TcpConnection(const TcpConnection&) = delete;
    TcpConnection& operator=(const TcpConnection&) = delete;

    TcpConnection(TcpConnection&& other) noexcept;
    TcpConnection& operator=(TcpConnection&& other) noexcept;

    void send(const std::vector<uint8_t>& data);
    std::vector<uint8_t> recv(size_t bufferSize = 4096);

private:
    std::unique_ptr<WinsockContext> m_context;
    SOCKET m_socket;
};
