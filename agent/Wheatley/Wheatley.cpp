#include <iostream>
#include <WheatleyAgent.hpp>

int main()
{
    std::unique_ptr<WheatleyAgent> agent = std::make_unique<WheatleyAgent>();
    agent->connect("127.0.0.1", 0x3333);
    auto request = agent->recvCommandRequest();
    auto response = agent->processCommandRequest(request);
    agent->sendCommandResponse(response);
}