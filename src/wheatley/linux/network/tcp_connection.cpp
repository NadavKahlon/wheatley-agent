#include <wheatley/common/network/tcp_connection.hpp>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cerrno>
#include <cstring>

using namespace wheatley::network;

TcpConnection::TcpConnection(const std::string& ip, int port) :
    m_context(std::make_unique<Context>()),
    m_socket(-1)
{
    m_socket = socket(AF_INET, SOCK_STREAM, 0);

    if (m_socket < 0) {
        throw std::runtime_error("Socket creation failed: " + std::string(strerror(errno)));
    }

    sockaddr_in serverAddr = {};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(static_cast<unsigned short>(port));

    if (inet_pton(AF_INET, ip.c_str(), &serverAddr.sin_addr) <= 0) {
        close(m_socket);
        throw std::runtime_error("Invalid IP address format or address not supported.");
    }

    if (connect(m_socket, reinterpret_cast<struct sockaddr*>(&serverAddr), sizeof(serverAddr)) < 0) {
        int err = errno;
        close(m_socket);
        throw std::runtime_error("Connection failed: " + std::string(strerror(err)));
    }
}

TcpConnection::~TcpConnection() {
    if (m_socket != -1) {
        close(m_socket);
        m_socket = -1;
    }
}

TcpConnection::TcpConnection(TcpConnection&& other) noexcept :
    m_context(std::move(other.m_context)),
    m_socket(other.m_socket)
{
    other.m_socket = -1;
}

TcpConnection& TcpConnection::operator=(TcpConnection&& other) noexcept {
    if (this != &other) {
        if (m_socket != -1) {
            ::close(m_socket);
        }

        m_context = std::move(other.m_context);
        m_socket = other.m_socket;
        other.m_socket = -1;
    }
    return *this;
}

void TcpConnection::send(const std::vector<uint8_t>& data) {
    ssize_t bytesSent = ::send(m_socket, data.data(), data.size(), 0);
    if (bytesSent < 0) {
        throw std::runtime_error("Send failed: " + std::string(strerror(errno)));
    }
}

std::vector<uint8_t> TcpConnection::recv(size_t bufferSize) {
    std::vector<uint8_t> buffer(bufferSize);
    ssize_t bytesRead = ::recv(m_socket, buffer.data(), bufferSize, 0);

    if (bytesRead < 0) {
        throw std::runtime_error("Recv failed: " + std::string(strerror(errno)));
    }
    else if (bytesRead == 0) {
        return {};
    }

    buffer.resize(static_cast<size_t>(bytesRead));
    return buffer;
}

std::vector<uint8_t> TcpConnection::recvExactly(size_t len)
{
    std::vector<uint8_t> buffer(len);
    size_t totalRead = 0;
    while (totalRead < len) {
        ssize_t bytesRead = ::recv(m_socket,
            buffer.data() + totalRead,
            len - totalRead, 0);
        if (bytesRead < 0) {
            throw std::runtime_error("Recv failed: " + std::string(strerror(errno)));
        }
        if (bytesRead == 0) {
            buffer.resize(totalRead);
            return buffer;
        }
        totalRead += static_cast<size_t>(bytesRead);
    }
    return buffer;
}
