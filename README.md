# inlinec
Simple inline C library for Python

## Usage

You can simply use the C-style code inside of your Python functions. Just use C decorator and make sure you returned the string of C code.
You will need pre-installed gcc/g++/clang compiler and correct path environment variable (for example ``CC='clang'``).

## Example 1.
```python
from inlinec import C

@C
def factorial(x):
    return ("""
    int factorial(int x) {
        int result = 1;
        while (x > 1) {
            result *= x;
            x--;
        }
    return result;
    }
""")

print(factorial(10))
# Output: 3628800
```

## Example 2.
```python
@C
def factorial(n):
    return ("""
    #import <stdio.h>
    #define MAX 500

    int multiply(int x, int res[], int res_size);

    void factorial(int n) {
        int res[MAX];
        static int fac[MAX];

        res[0] = 1;
        int res_size = 1;

        for (int x=2; x<=n; x++)
            res_size = multiply(x, res, res_size);

        for (int i=res_size-1; i>=0; i--)
            printf("%d", res[i]);
    }

    int multiply(int x, int res[], int res_size) {
        int carry = 0;

        for (int i=0; i<res_size; i++) {
            int prod = res[i] * x + carry; 

            res[i] = prod % 10; 

            carry = prod/10;
        }

        while (carry) {
            res[res_size] = carry%10; 
            carry = carry/10; 
            res_size++; 
        }
        return res_size; 
    }
""")

factorial(10)
# Output: 3628800
```

# How does this work?

The ``C`` class inserts C code directly into the Python files, which can then be dynamically linked and called via ctypes. 

Note that all libraries given (they are assumed to be shared libraries) are also linked into the shared library, and thus loaded into the current program as well.

# Limitations

*Note: This is just a proof of concept.*

**Please do not hesitate fork this project and make some changes.**

1. Python function should have the same name as the C one.
2. It is better to return only one C function from the Python def.
> In principle you could use more than one (see Example 2), but you need to specify which function you would like to link with the Python.
3. Many more.

# To do
- [x] fix argtypes
- [x] fix restypes
- [ ] add dictionary for all variable types (long long, unsigned short, pointers, etc)
- [ ] fix bug when you define function as ``def test(a=1, b=1.0, c=b'a'): pass`` and further call it ``test(x=1, y=1.0, z=b'a')`` with another set of parameters (but types should be the same)
- [ ] add tests
- [ ] fix ``_argconstructor`` (this one is works but probably not ideally)
