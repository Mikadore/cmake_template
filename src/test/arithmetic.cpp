import arithmetic;

#include <catch2/catch_test_macros.hpp>


TEST_CASE("Arithmetic")
{
    REQUIRE(add(1, 1) == 2);
    REQUIRE(mul(2, 3) == 6);
}
