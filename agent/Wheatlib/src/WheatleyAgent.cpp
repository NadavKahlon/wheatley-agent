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

agent::command::Request WheatleyAgent::recvCommand()
{
	if (!m_connection) {
		throw std::runtime_error("Agent is not connected to a server.");
	}
	return m_connection->recvProtobuf<agent::command::Request>();
}
