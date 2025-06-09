import os
import CppHeaderParser

# Path of current script
base_dir = os.path.dirname(__file__)
header_path = os.path.join(base_dir, "DummySrc.hpp")

print("Loading header from:", header_path)
header = CppHeaderParser.CppHeader(header_path)
for cls in header.classes.values():
    print(f"class {cls['name']}:")
    for method in cls["methods"]["public"]:
        print(
            f"  {method['name']}({', '.join(p['type'] for p in method['parameters'])})"
        )


def generate_binding(header_path, output_dir):
    header = CppHeaderParser.CppHeader(header_path)
    for cls in header.classes.values():
        class_name = cls["name"]
        bind_filename = os.path.join(output_dir, f"bind_{class_name}.cpp")
        with open(bind_filename, "w") as f:
            f.write("#include <pybind11/pybind11.h>\n")
            f.write(f'#include "{os.path.basename(header_path)}"\n\n')
            f.write("namespace py = pybind11;\n\n")
            f.write(f"void bind_{class_name}(py::module_& m) {{\n")
            f.write(f'    py::class_<{class_name}>(m, "{class_name}")\n')

            for method in cls["methods"]["public"]:
                if method["constructor"]:
                    f.write("        .def(py::init<>())\n")
                else:
                    f.write(
                        f'        .def("{method["name"]}", &{class_name}::{method["name"]})\n'
                    )
            f.write("    ;\n}\n")
