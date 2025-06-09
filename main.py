import sys
from pathlib import Path

# Point Python to the exact folder containing sonycam.pyd
sys.path.append(str(Path(__file__).parent / "bindings" / "build" / "Debug"))

import sonycam


def main():
    a = 10
    b = 20
    op = sonycam.MathOps()
    print("\nUsing sonycam")
    sonycam.sayHello()
    print(f"\nadd: {op.add(a, b)}")
    print(f"\nsub: {op.subtract(a, b)}")
    print(f"\nmul: {op.multiply(a, b)}")
    print(f"\ndiv: {op.divide(a, b)}")


if __name__ == "__main__":
    main()
