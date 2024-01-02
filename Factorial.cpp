#include <format>
#include <iostream>

using std::format;
using std::cout;

unsigned long factorial(unsigned long number) {
	unsigned long result{ number };
	if (number < 0) return 0;
	if (number == 1) return number;
	if (0 > number) return 0;
	while (number > 2) {
		result *= (number - 1);
		number--;
	}
	return result;
}

int main() {
	unsigned long number; 
	std::cin >> number;
	cout << format("The factorial of {} is {} \n", number, factorial(number));

}