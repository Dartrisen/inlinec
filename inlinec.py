import os
from re import search, findall, match
from shlex import quote
from atexit import register
from sys import stderr, exit
from tempfile import NamedTemporaryFile, mktemp
from inspect import getfullargspec, formatargspec, getargspec
from ctypes import cdll
from consts import types, arg_pattern, res_pattern


try:
    os.environ['CC'] = 'clang'
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
        self.args = formatargspec(*getfullargspec(func))
        self.defaults = getfullargspec(func).defaults
        self._compile(self.func(self.args), shared_libs)

    def __call__(self, *args, **kwargs):
        name = self.func.__name__
        defaults = self.defaults or tuple()
        self.__getitem__(name).argtypes = self._argparser()
        self.__getitem__(name).restype = self._resparser()
        args = self._argconstructor(args, kwargs)
        if args == defaults:
            return self.__getitem__(name)(*args)
        else:
            args = args + defaults
            return self.__getitem__(name)(*args)

    def _argparser(self):
        string = self.func(self.args)
        text = search(r'\((.*?)\)', string).group(1)
        text = findall(arg_pattern, text)
        return [types[type_] for type_ in text]

    def _resparser(self):
        string = self.func(self.args)
        text = search(res_pattern, string).group(1)
        return types[text]

    def _argconstructor(self, args, kwargs):
        args = args or tuple()
        kwargs = tuple(kwargs.values()) or tuple()
        return args + kwargs

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
