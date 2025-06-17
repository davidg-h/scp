import os
import CppHeaderParser

# Path to the current script and target header
base_dir = os.path.dirname(__file__)
header_path = os.path.join(base_dir, "src.hpp")  # Change to match your actual header
module_name = "sonycam"


def generate_bindings(header_path):
    try:
        cpp = CppHeaderParser.CppHeader(header_path)
    except CppHeaderParser.CppParseError as e:
        print(f"Failed to parse header: {e}")
        return ""

    lines = [
        "#include <pybind11/pybind11.h>",
        f'#include "{os.path.basename(header_path)}"',
        "",
        "namespace py = pybind11;",
        "",
        f"PYBIND11_MODULE({module_name}, m) " + "{",
    ]

    # Bind #define macros (constants)
    for define in cpp.defines:
        try:
            name, value = define.split(maxsplit=1)
            lines.append(f'    m.attr("{name}") = {value};')
        except ValueError:
            # Handle cases like `#define SOMETHING` (no value)
            lines.append(f'    m.attr("{define.strip()}") = py::none();')

    # Bind const/static global variables
    for var in cpp.variables:
        if var.get("const", False) or var.get("static", False):
            lines.append(f'    m.attr("{var["name"]}") = {var["name"]};')

    # Bind global functions
    for func in cpp.functions:
        lines.append(f'    m.def("{func["name"]}", &{func["name"]});')

    # Bind classes and their methods
    for cls in cpp.classes.values():
        lines.append(f'    py::class_<{cls["name"]}>(m, "{cls["name"]}")')
        lines.append("        .def(py::init<>())")
        for method in cls["methods"]["public"]:
            if not method.get("constructor", False):
                lines.append(
                    f'        .def("{method["name"]}", &{cls["name"]}::{method["name"]})'
                )
        lines[-1] += ";"  # Add ; to last .def

    for enum in cpp.enums:
        enum_name = enum["name"]
        enum_scope = enum.get("namespace", "").strip(":")
        full_enum_name = f"{enum_scope}::{enum_name}" if enum_scope else enum_name

        lines.append(f'    py::enum_<{full_enum_name}>(m, "{enum_name}")')
        for val in enum["values"]:
            lines.append(
                f'        .value("{val["name"]}", {full_enum_name}::{val["name"]})'
            )
        lines.append("        .export_values();")

    lines.append("}")
    return "\n".join(lines)


# Output the result
print(f"\nGenerating bindings for {header_path}...\n\n")

bindings_code = generate_bindings(header_path)
print(bindings_code)


# Output path for the generated bindings file
output_path = os.path.join(base_dir, "bindings.cpp")

# Write to file
with open(output_path, "w") as f:
    f.write(bindings_code)

print(f"\n✅ bindings.cpp has been generated at: {output_path}")
