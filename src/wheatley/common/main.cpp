#include <iostream>
#include <wheatley/common/agent.hpp>

int main()
{
    FILE* stream;
    (void)freopen_s(&stream, "NUL", "w", stderr);
    std::unique_ptr<wheatley::Agent> agent = std::make_unique<wheatley::Agent>();
    while (true) {
        try {
            agent->run("127.0.0.1", 0x3333);
        }
        catch (const std::runtime_error&) {}
        if (agent->wasDestroyed) {
            break;
        }
        agent = std::make_unique<wheatley::Agent>();
        printf("Restarted\n");
    }
}
