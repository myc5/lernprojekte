// Print out all prime numbers between 0 and 100

#include <format> // requires C++ 20+
#include <iostream>

using std::format;
using std::cout;

int num = 2;
int arr[30]{}; // auto sized array how?
int array_num = 0;
int divisor = 2;
bool primeFlag = true;


int main() {
	while (num <= 100) {
		for (divisor = 2; divisor < num; divisor++) { // exclude numbers 0 and 1 since they cannot be primes
			if (num % divisor == 0) { // if the number can ever be wholly divided by a divisor that is smaller than itself and not prime
				primeFlag = false;
				break; // break out of the loop and set prime flag to false
			}
		}
			if (primeFlag) { // if it went through the whole loop above and flag is still set to true, add it to the array
				arr[array_num] = num;
				array_num++; // increment array index
			}
	primeFlag = true;
	num++;

	}
	int counter = 0;
	for (const int& i : arr) {
		if (i) { // as long as there are non-zero elements left, print them out
			cout << format("{}\n", i);
			counter++;
		}
		else { // "0" indicates the end, print that out and tell user how oversized the array was until we figure out how to auto size one
			cout << format("Reached end of array at index {}, leaving {} array slots empty", counter, 30 - counter);
			break;
		}
	}
}
