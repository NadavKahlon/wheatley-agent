#include <stdexcept>
#include <WS2tcpip.h>
#include <wheatley/common/network/tcp_connection.hpp>

using namespace wheatley::network;


TcpConnection::TcpConnection(const std::string& ip, int port) : 
        m_context(std::make_unique<Context>()),
        m_socket(INVALID_SOCKET)
{
    m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (m_socket == INVALID_SOCKET) {
        throw std::runtime_error("Socket creation failed: " + std::to_string(WSAGetLastError()));
    }

    sockaddr_in serverAddr = {};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(static_cast<unsigned short>(port));

    if (inet_pton(AF_INET, ip.c_str(), &serverAddr.sin_addr) <= 0) {
        closesocket(m_socket);
        throw std::runtime_error("Invalid IP address format.");
    }

    if (connect(m_socket, reinterpret_cast<struct sockaddr*>(&serverAddr), sizeof(serverAddr)) == SOCKET_ERROR) {
        int error = WSAGetLastError();
        closesocket(m_socket);
        throw std::runtime_error("Connection failed: " + std::to_string(error));
    }
}

TcpConnection::~TcpConnection() {
    if (m_socket != INVALID_SOCKET) {
        closesocket(m_socket);
        m_socket = INVALID_SOCKET;
    }
}

TcpConnection::TcpConnection(TcpConnection&& other) noexcept :
    m_context(std::move(other.m_context)),
    m_socket(other.m_socket)
{
    other.m_socket = INVALID_SOCKET;
}

TcpConnection& TcpConnection::operator=(TcpConnection&& other) noexcept {
    if (this != &other) {
        if (m_socket != INVALID_SOCKET) {
            ::closesocket(m_socket);
        }

        m_context = std::move(other.m_context);
        m_socket = other.m_socket;

        other.m_socket = INVALID_SOCKET;
    }
    return *this;
}

void TcpConnection::send(const std::vector<uint8_t>& data) {
    int bytesSent = ::send(m_socket, reinterpret_cast<const char*>(data.data()), static_cast<int>(data.size()), 0);
    if (bytesSent == SOCKET_ERROR) {
        throw std::runtime_error("Send failed: " + std::to_string(WSAGetLastError()));
    }
}

std::vector<uint8_t> TcpConnection::recv(size_t bufferSize) {
    std::vector<uint8_t> buffer(bufferSize);
    int bytesRead = ::recv(m_socket, reinterpret_cast<char*>(buffer.data()), static_cast<int>(bufferSize), 0);

    if (bytesRead == SOCKET_ERROR) {
        throw std::runtime_error("Recv failed: " + std::to_string(WSAGetLastError()));
    }
    else if (bytesRead == 0) {
        return {};
    }

    buffer.resize(bytesRead);
    return buffer;
}

std::vector<uint8_t> TcpConnection::recvExactly(size_t len)
{
    std::vector<uint8_t> buffer(len);
    size_t totalRead = 0;
    while (totalRead < len) {
        int bytesRead = ::recv(m_socket,
            reinterpret_cast<char*>(buffer.data() + totalRead),
            static_cast<int>(len - totalRead), 0
        );
        if (bytesRead == SOCKET_ERROR) {
            throw std::runtime_error("Recv failed: " + std::to_string(WSAGetLastError()));
        }
        if (bytesRead == 0) {
            // Peer closed connection - return whatever we got
            buffer.resize(totalRead);
            return buffer;
        }
        totalRead += bytesRead;
    }
    return buffer;
}
