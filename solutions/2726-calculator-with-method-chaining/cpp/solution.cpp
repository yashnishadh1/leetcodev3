#include <cmath>
#include <stdexcept>

class Calculator {
private:
    double result;

public:
    Calculator(double value) : result(value) {}

    Calculator& add(double value) {
        result += value;
        return *this;
    }

    Calculator& subtract(double value) {
        result -= value;
        return *this;
    }

    Calculator& multiply(double value) {
        result *= value;
        return *this;
    }

    Calculator& divide(double value) {
        if (value == 0) {
            throw std::invalid_argument("Division by zero is not allowed");
        }
        result /= value;
        return *this;
    }

    Calculator& power(double value) {
        result = std::pow(result, value);
        return *this;
    }

    double getResult() const {
        return result;
    }
};

class Solution {
};
