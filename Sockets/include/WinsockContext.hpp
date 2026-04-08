#pragma once

class WinsockContext {
public:
    WinsockContext();
    ~WinsockContext();

    // Disable copying for RAII integrity
    WinsockContext(const WinsockContext&) = delete;
    WinsockContext& operator=(const WinsockContext&) = delete;
};
