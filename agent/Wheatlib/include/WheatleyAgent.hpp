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

    void connect(const std::string& ip, int port);
    void disconnect();

    agent::command::Request recvCommand();

private:
    std::unique_ptr<TcpConnection> m_connection;
};
