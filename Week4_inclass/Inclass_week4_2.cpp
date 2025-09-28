#include <iostream>
#include "math.h"

int main() {
    int x, y;
    std::cout << "Enter two numbers: ";
    std::cin >> x >> y;
    std::cout << "sum: " << add(x, y) << std::endl;
    return 0;
}
