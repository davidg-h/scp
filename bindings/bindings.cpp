#include <pybind11/pybind11.h>
#include "DummySrc.hpp"

namespace py = pybind11;

PYBIND11_MODULE(sonycam, m)
{
    m.def("sayHello", &sayHello, "A function that prints a greeting message");
    py::class_<MathOps>(m, "MathOps")
        .def(py::init<>())
        .def("add", &MathOps::add, "A method that adds two numbers")
        .def("multiply", &MathOps::multiply, "A method that multiplies two numbers")
        .def("subtract", &MathOps::subtract, "A method that subtracts two numbers")
        .def("divide", &MathOps::divide, "A method that divides two numbers");
}
