#include <iostream>
#include <WheatleyAgent.hpp>

int main()
{
    while (true) {
        try {
            std::unique_ptr<WheatleyAgent> agent = std::make_unique<WheatleyAgent>();
            agent->run("127.0.0.1", 0x3333);
        }
        catch (const std::runtime_error& e) {}
    }
}
