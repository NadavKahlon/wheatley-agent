#pragma once

namespace wheatley::network {

class Context {
public:
    Context();
    ~Context();

    // Disable copying for RAII integrity
    Context(const Context&) = delete;
    Context& operator=(const Context&) = delete;
};

}
