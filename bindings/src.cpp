#include <iostream>
#include "DummySrc.hpp"

void sayHello()
{
    std::cout << "Hello from DummySrc!" << std::endl;
}

int MathOps::add(int a, int b)
{
    return a + b;
}

int MathOps::multiply(int a, int b)
{
    return a * b;
}

int MathOps::subtract(int a, int b)
{
    return a - b;
}

float MathOps::divide(int a, int b)
{
    if (b == 0)
    {
        std::cerr << "Error: Division by zero!" << std::endl;
        return 0; // or throw an exception
    }
    return (float)a / b;
}