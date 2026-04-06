#include <WheatleyAgent.hpp>
#include <WheatleyProto.hpp>
#include <stdexcept>

WheatleyAgent::WheatleyAgent() : m_connection(nullptr)
{
}

WheatleyAgent::~WheatleyAgent()
{
}

void WheatleyAgent::connect(const std::string& ip, int port)
{
	m_connection.reset(new TcpConnection(ip, port));
}

void WheatleyAgent::disconnect()
{
	m_connection.reset(nullptr);
}

agent::command::Request WheatleyAgent::recvCommandRequest()
{
	if (!m_connection) {
		throw std::runtime_error("Agent is not connected to a server.");
	}
	return m_connection->recvProtobuf<agent::command::Request>();
}

agent::command::Response WheatleyAgent::processCommandRequest(agent::command::Request request)
{
    agent::command::Response response;
    switch (request.request_case()) {

    // Health check command handler
    case agent::command::Request::kHealthCheck: {
        response.mutable_health_check();
        break;
    }

    case agent::command::Request::REQUEST_NOT_SET:
    default:
        throw std::runtime_error("Request type not set.");
    }

    return response;
}

void WheatleyAgent::sendCommandResponse(agent::command::Response response)
{
	if (!m_connection) {
		throw std::runtime_error("Agent is not connected to a server.");
	}
	m_connection->sendProtobuf(response);
}
