import convert;

#include <catch2/catch_test_macros.hpp>

TEST_CASE("Convert")
{
    REQUIRE(parse_i32("0") == 0);
    REQUIRE(parse_i32("-1") == -1);
    REQUIRE(parse_i32("1") == 1);
}
