# inlinec
Inline C library for Python

## Usage

You can simply use the C-style code inside of your Python functions.

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

# Limitations

Note: This is just a proof of concept. Please do not hesitate fork this project and make some changes.

1. Python function should have the same name as the C one.
2. Only one C function per Python one (in fact you could use more than one, but you need to be sure that your "main" C function has the same name as Python).
3. Many more.
