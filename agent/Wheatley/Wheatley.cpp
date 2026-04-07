#include <iostream>
#include <WheatleyAgent.hpp>

int main()
{
    FILE* stream;
    (void)freopen_s(&stream, "NUL", "w", stderr);
    std::unique_ptr<WheatleyAgent> agent = std::make_unique<WheatleyAgent>();
    while (true) {
        try {
            agent->run("127.0.0.1", 0x3333);
        }
        catch (const std::runtime_error&) {}
        if (agent->wasDestroyed) {
            break;
        }
        std::unique_ptr<WheatleyAgent> agent = std::make_unique<WheatleyAgent>();
    }
}
