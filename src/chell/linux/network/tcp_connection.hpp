#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <memory>
#include <stdexcept>
#include <cstring>
#include <arpa/inet.h>  // For htons, htonl, etc.
#include <chell/common/network/context.hpp>
#include <google/protobuf/message.h>

namespace chell::network {

class TcpConnection {
public:
    TcpConnection(const std::string& ip, int port);
    ~TcpConnection();

    TcpConnection(const TcpConnection&) = delete;
    TcpConnection& operator=(const TcpConnection&) = delete;

    TcpConnection(TcpConnection&& other) noexcept;
    TcpConnection& operator=(TcpConnection&& other) noexcept;

    void send(const std::vector<uint8_t>& data);
    std::vector<uint8_t> recv(size_t bufferSize = 4096);
    std::vector<uint8_t> recvExactly(size_t len);

private:
    std::unique_ptr<Context> m_context;
    int m_socket;
};

}