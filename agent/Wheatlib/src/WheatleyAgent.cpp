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

    // Command execution handler
    case agent::command::Request::kExecute: {
        auto output = handleExecute(request.execute().command());
        response.mutable_execute()->set_output(output);
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

std::string WheatleyAgent::handleExecute(const std::string &command)
{
    std::array<char, 128> buffer;
    std::string result;
    auto pipe = _popen(command.c_str(), "r");
    if (!pipe) {
        return "Error: Failed to open pipe for command execution.";
    }
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        result += buffer.data();
    }
    _pclose(pipe);
    return result;
}
