class Calculator {
    private double result;

    public Calculator(double value) {
        this.result = value;
    }

    public Calculator add(double value) {
        this.result += value;
        return this;
    }

    public Calculator subtract(double value) {
        this.result -= value;
        return this;
    }

    public Calculator multiply(double value) {
        this.result *= value;
        return this;
    }

    public Calculator divide(double value) {
        if (value == 0) {
            throw new ArithmeticException("Division by zero is not allowed");
        }
        this.result /= value;
        return this;
    }

    public Calculator power(double value) {
        this.result = Math.pow(this.result, value);
        return this;
    }

    public double getResult() {
        return this.result;
    }
}

class Solution {
}
