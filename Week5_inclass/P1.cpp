#include <iostream>
#include<string>

int main()
{
	std::string num_a;
	std::string num_b;

	std::cout << "Enter first number: ";
	std::cin >> num_a;

	std::cout << "Enter second number: ";	
	std::cin >> num_b;	

	std::string reversed_a;
	std::string reversed_b;	

	for (int i = num_a.length()-1; i >= 0 ; --i) {
		reversed_a += num_a[i];
	}

	for (int i = num_b.length() - 1; i >= 0; --i) {
		reversed_b += num_b[i];
	}
	std::cout << "Reversed first number: " << reversed_a << std::endl;
	std::cout << "Reversed second number: " << reversed_b << std::endl;

	if (reversed_a > reversed_b) {
        std::cout << "더 큰 숫자는: " << reversed_a << std::endl;
    } 
	else {
        std::cout << "더 큰 숫자는: " << reversed_b << std::endl;
    }
	
}
