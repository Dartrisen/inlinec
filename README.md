# inlinec
Simple inline C library for Python

## Usage

You can simply use the C-style code inside of your Python functions. Just use C decorator and make sure you returned the string of C code.
You will need pre-installed gcc/g++/clang compiler and correct path environment variable (for example CC='clang').

```python
from inlinec import C

@C
def factorial(x):
    return ('''
    int factorial(int x) {
        int result = 1;
        while (x > 1) {
            result *= x;
            x--;
        }
    return result;
    }
''')

print(factorial(10))
# Output: 3628800
```

# How does this work?

The ``C`` class inserts C code directly into the Python files, which can then be dynamically linked and called via ctypes. 

Note that all libraries given (they are assumed to be shared libraries) are also linked into the shared library, and thus loaded into the current program as well.

# Limitations

Note: This is just a proof of concept.

**Please do not hesitate fork this project and make some changes.**

1. Python function should have the same name as the C one.
2. It is better to return only one C function from the Python def (in principle you could use more than one, but you need to be sure that your "main" C function has the same name as Python).
3. Do not use ``(x: int, y: float)`` styling...
4. Many more.

# To do
1. add dictionary for all variable types (long long, unsigned short, etc)
2. fix bug when you can define function ``def test(a=1, b=1.0, c=b'a'): pass`` and further call it ``test(x=1, y=1.0, z=b'a')`` with another set of parameters (but types should be the same)
3. add tests
4. fix ``_argconstructor`` (this one is works but probably not ideally)
5. fix ``restype``
