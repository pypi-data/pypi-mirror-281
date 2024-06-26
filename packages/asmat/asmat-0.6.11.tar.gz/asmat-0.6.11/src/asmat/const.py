import os

root = os.getcwd()

settings = f"{root}/settings.json"


ARCH = {
    'sse' : '-msse', 
    'sse2' : '-msse2',
    'sse3' : '-msse3',
    'sse4.2' : '-msse4.2', 
    'ssse3' : '-mssse3',
    'avx' : '-mavx',
    'avx2' : '-mavx2',
    'avx512' : '-march=skylake-avx512'}


COMPILER = {
    'clang' : 'clang',
    'gcc' : 'g++'
}


OPTIONS = {
    "validate" : True,
    "log" : False,
    "deep" : False,
    "input" : 'all',
    "keep_tmp" : False,
    "generate" : False,
    "exception" : False,
    "verbose" : False,
    "disassembler" : "objdump",
    "instruction_comparison" : False,
    "flags" : [],
    "setup" : None,
    "compiler" : None,
    "output" : f"{root}/ref",
    "limit_per_file" : 'inf',
    "nbprocess" : 0,
    "headers" : []
}


REAL = ['float', 'double']
SIGNED_INTEGER = ['std::int64_t', 'std::int32_t', 'std::int16_t', 'std::int8_t']
UNSIGNED_INTEGER = ["std::uint64_t" , "std::uint32_t" , "std::uint16_t" , "std::uint8_t"]
INTEGER = SIGNED_INTEGER + UNSIGNED_INTEGER
SIGNED = SIGNED_INTEGER + REAL

ARITHMETIC = REAL + INTEGER + UNSIGNED_INTEGER


# Densité arithmétique memory access / instructions