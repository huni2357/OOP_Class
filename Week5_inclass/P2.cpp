#include <iostream>
#include<string>

namespace {
    void log_calculation(int result) {
        std::cout << "LOG: Calculation performed, result is " << result << std::endl;
    }
}

namespace OOPCourse::Math {
   .
    int add_and_log(int a, int b) {
        int result = a + b;
        log_calculation(result);
        return result;
    }
}

int main() {

    using OOPCourse::Math::add_and_log;
    std::cout << "Calling the public API function..." << std::endl;
    int final_result = add_and_log(15, 27);
   
    std::cout << "The value returned by add_and_log(15, 27) is: " << final_result << std::endl;

    return 0;
}
