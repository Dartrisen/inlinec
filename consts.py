from ctypes import c_char, c_int, c_float, c_double, c_bool, c_short, c_long, c_size_t

types = {'char'     : c_char,
         'int'      : c_int,
         'float'    : c_float,
         '_Bool'    : c_bool,
         'double'   : c_double,
         'short'    : c_short,
         'long'     : c_long,
         'size_t'   : c_size_t,
         'void'     : None}

arg_pattern = r'(char|int|float|_Bool|double|short|long|size_t)+ \w+'
res_pattern = r'(void|char|int|float|_Bool|double|short|long|size_t)\s'
