import os
from ctypes import cdll
from shlex import quote
from atexit import register
from sys import stderr, exit
from inspect import getfullargspec
from tempfile import NamedTemporaryFile, mktemp

try:
    # if you're using the clang compiler
    # os.environ['CC'] = 'clang'
    COMPILER = os.environ['CC']
except KeyError:
    print('CC environment variable must point to C compiler', file=stderr)
    exit(1)

CMDLINE_C_TO_OBJ = '{compiler} -c -o {output} {input}'

CMDLINE_OBJ_TO_SO = '{compiler} -shared -o {output} {input} {libraries}'

class C:
    def __init__(self, func, *shared_libs):
        self.func = func
        self.library = None
        self.args = getfullargspec(func)
        self._compile(self.func(self.args), shared_libs)

    def __call__(self, *args, **kwargs):
        name = self.func.__name__
        if args:
            return self.__getitem__(name)(*args)
        elif kwargs:
            return self.__getitem__(name)(*kwargs.values())
        else:
            return self.__getitem__(name)(*self.args.defaults)

    def _compile(self, code, libs):
        with NamedTemporaryFile(mode='w', prefix='PYC', suffix='.c',
                                delete=False) as temp_c_file:
            temp_c_file_name = temp_c_file.name

            temp_c_file.write(code)
            temp_c_file.flush()

        obj_file_name = mktemp(prefix='PYC', suffix='.o')
        os.system(CMDLINE_C_TO_OBJ.format(compiler=COMPILER, 
            output=quote(obj_file_name), 
            input=quote(temp_c_file_name))
        )
        os.remove(temp_c_file_name)

        so_file_name = mktemp(prefix='PYC', suffix='.so')
        library_cmd = ' '.join('-l' + lib for lib in libs)
        os.system(CMDLINE_OBJ_TO_SO.format(compiler=COMPILER,
            output=quote(so_file_name),
            input=quote(obj_file_name),
            libraries=library_cmd)
        )
        os.remove(obj_file_name)

        self.library = cdll.LoadLibrary(so_file_name)

        register(lambda: os.remove(so_file_name))

    def __getitem__(self, func):
        if self.library is None:
            assert (False, "How did C.__getitem__ get called without loading the library?")

        return getattr(self.library, func)
