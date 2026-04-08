#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <winsock.h>
#include <memory>
#include <stdexcept>
#include <WinsockContext.hpp>
#include <google/protobuf/message.h>

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
    std::vector<uint8_t> recvExactly(size_t len);

    template <typename T>
    void sendProtobuf(const T& message) {
        static_assert(std::is_base_of_v<google::protobuf::Message, T>, "T must be a Protobuf message");

        // Set 4-byte size prefix of the message
        const size_t payloadSize = message.ByteSizeLong();
        const uint32_t netSize = htonl(static_cast<uint32_t>(payloadSize));

        // Set buffer to hold the message with the 4-byte size prefix
        std::vector<uint8_t> buffer(sizeof(netSize) + payloadSize);
        std::memcpy(buffer.data(), &netSize, sizeof(netSize));

        // Serialize the protobuf into the rest of the message
        if (!message.SerializeToArray(buffer.data() + sizeof(netSize), static_cast<int>(payloadSize))) {
            throw std::runtime_error("Failed to serialize protobuf message.");
        }
        send(buffer);
    }

    template <typename T>
    T recvProtobuf() {
        static_assert(std::is_base_of_v<google::protobuf::Message, T>, "T must be a Protobuf message");

        // Receive 4-byte size prefix
        std::vector<uint8_t> header = recvExactly(sizeof(uint32_t));
        if (header.empty()) {
            throw std::runtime_error("Connection closed while reading header.");
        }
        uint32_t netSize;
        std::memcpy(&netSize, header.data(), sizeof(uint32_t));
        const uint32_t payloadSize = ntohl(netSize);

        // Sanity check for payloadSize
        // TODO Magic
        if (payloadSize > 64 * 1024 * 1024) {
            throw std::runtime_error("Payload size too large.");
        }

        // Handle empty messages (valid in Protobuf)
        T message;
        if (payloadSize == 0) return message;

        // Receive and deserialize
        std::vector<uint8_t> payload = recvExactly(payloadSize);
        if (payload.size() < payloadSize) {
            throw std::runtime_error("Connection closed before receiving full payload.");
        }
        if (!message.ParseFromArray(payload.data(), static_cast<int>(payloadSize))) {
            throw std::runtime_error("Failed to deserialize protobuf message.");
        }

        return message;
    }

private:
    std::unique_ptr<WinsockContext> m_context;
    SOCKET m_socket;
};
