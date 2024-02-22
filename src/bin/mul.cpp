import arithmetic;
import convert;
import std_imports;

#include <fmt/core.h>
#include <span>

auto main(int argc, char* argv[]) -> int {
    if (argc < 3) {
        fmt::print("usage: ./mul x y");
        return 1;
    }       
    auto args = std::span(argv, static_cast<usize>(argc));
    
    auto x = parse_i32(args[1]);   
    auto y = parse_i32(args[2]);  
    fmt::print("{} + {} = {}\n", x, y, mul(x, y));
}