from asmat.generation import *
import os
import asmat.reader as reader
import time
import asmat.const as const
from asmat.option import setup


LOG_PATH = f"{const.root}/log.txt"


class AssemblyMismatch(Exception):
    """Assembly mismatch exception

    Args:
        Exception (str, str, str, list, list): Raised when -r option is True.
    """
    def __init__(self, function:str, compiler:str, arch:str, expected:list, actual:list, *args: object) -> None:
        super().__init__(*args)
        self.function = function
        self.compiler = compiler
        self.arch = arch
        self.expected = expected
        self.actual = actual

    def format_instructions(self, instr):
        s = ""
        for i in instr:
            s = s + '\t' + i['instr'] + '\n'
        return s

    def __str__(self) -> str:
        s0 = f'\n-------------------------------------------------\nAssembly mismatch with function : {self.function}\n\n'
        s1 = f'Compiler : {self.compiler}\nArchitecture : {self.arch}\n'
        #s2 = 'Expecting :\n' + self.format_instructions(self.expected) + '\n'
        #s3 = 'Got:\n' + self.format_instructions(self.actual) + '\n'

        return s0 + s1 #+ s2 + s3



def log_unmatched_instruction(function:str, compiler:str, arch:str, types:list, expected:list, actual:list):
    """Format function for the log file.

    Args:
        function (str): Function name.
        compiler (str): Compiler name.
        arch (str): Architecture name.
        types (list): List of parameters types.
        expected (list): List of expected assembly.
        actual (list): List of actual assembly.

    Returns:
        str: Log string.
    """

    s = f'-----------------------------\nFunction : {function}\nCompiler : {compiler}\nArchitecture : {arch}\n'
    s += f'Parameters : {" ".join(types)}\n'
    s += f'\n\n\tExpected\tActual\n\n'
    for i in range(0, max(len(expected), len(actual))):
        if len(expected) <= i:
            s += f'--> ____ \t--> {actual[i]}\n'
        elif len(actual) <= i:
            s += f'--> {expected[i]} \t--> ____\n'
        else:
            if expected[i] != actual[i]:
                s += f'--> {expected[i]}\t--> {actual[i]}\n'
            else:
                s += f'\t{expected[i]}\t{actual[i]}\n'

    return s + '\n\n\n'





def log_undefined_reference(function:str, compiler:str, architecture:str):
    """Format undefined reference error for log file. 

    Args:
        function (str): Function name.
        compiler (str): Compiler name.
        architecture (str): Architecture name.

    Returns:
        str: Log string.
    """

    s = f'-----------------------------\nUndefined reference for function {function}\nCompiler : {compiler}\nArchitecture : {architecture}\n'
    s1 = "\nThis function has not been tested. Try generating reference using option -g\n\n"
    return s + s1





def validate_bis(options, conf={}) -> int:
    """Validation function. Generates assembly for the current library version and compares it with reference assembly.

    Args:
        options (_type_): Dictionary describing user query. The structure of the dictionary is stored in `const.OPTIONS`.
        conf (dict, optional): Configuration with all information about compilation targets. Defaults to {}.

    Raises:
        AssemblyMismatch: Raised when errors occur and raise_exception is True.

    Returns:
        int: 0 if process finished without errors, otherwise -1.
    """

    functions = []
    for k in conf.keys():
        for typ in conf[k]:
            functions.append((k, typ))

    functions_assembly = instructions.get_functions_instructions(options, functions)

    
    validation_set = reader.read_reference_files(options['input'], path=options['output'])

    ret = 0
    errors = 0
    log_txt = ""

    for c in functions_assembly.keys(): # compiler
        for a in functions_assembly[c].keys(): # simd extension
            for f in functions_assembly[c][a].keys(): # function
                if f not in validation_set[c][a].keys():
                    log_txt += log_undefined_reference(f, c, a)
                    if options['verbose']:
                        print(f"**WARNING** - Function {f} not found in references (comp {c}, {a}). Try generating using option -g.")
                    ret = -1
                elif not functions_assembly[c][a][f] == validation_set[c][a][f]:
                    for i in range(0, min(len(functions_assembly[c][a][f]), len(validation_set[c][a][f]))):
                        
                        # Compare only assembly instruction, ignore parameters
                        if options['instruction_comparison']:
                            for j in range(0, min(len(functions_assembly[c][a][f][i]['instr']), len(validation_set[c][a][f][i]['instr']))):
                                i1 = functions_assembly[c][a][f][i]['instr'][j].split(' ')[0]
                                i2 = validation_set[c][a][f][i]['instr'][j].split(' ')[0]
                                if i1 != i2:
                                    ret = -1
                                    errors += 1
                                    if options['exception']:
                                        raise AssemblyMismatch(f, c, a, validation_set[c][a][f][i]['type'], validation_set[c][a][f][i]['instr'], functions_assembly[c][a][f][i]['instr'])
                                    log_txt += log_unmatched_instruction(f, c, a, validation_set[c][a][f][i]['type'], validation_set[c][a][f][i]['instr'], functions_assembly[c][a][f][i]['instr'])
                            
                        elif functions_assembly[c][a][f][i] != validation_set[c][a][f][i]:
                            errors += 1
                            if options['exception']:
                                raise AssemblyMismatch(f, c, a, validation_set[c][a][f][i]['type'], validation_set[c][a][f][i]['instr'], functions_assembly[c][a][f][i]['instr'])
                            log_txt += log_unmatched_instruction(f, c, a, validation_set[c][a][f][i]['type'], validation_set[c][a][f][i]['instr'], functions_assembly[c][a][f][i]['instr'])
                            ret = -1

    # Log file optional
    if options['log'] and log_txt != "":
        if os.path.exists(LOG_PATH):
            file = open(LOG_PATH, 'w')
        else:
            file = open(LOG_PATH, 'x')
        file.write(log_txt)
        file.close()

    if options['verbose']:
        print(f"Process finished : {errors} mismatching function(s) found")

    return ret





def validate(options : dict | setup, max_function_files='inf') -> int:
    """Auxiliary function for validation. This function limits the function per file for compilation.

    Args:
        options (_type_): Dictionary describing user query. The structure of the dictionary is stored in `const.OPTIONS`.
        max_function_files (str, optional): The maximum number of function in a cpp file. A function is one config file (it can generate more than one if there are several\
              parameters configuration). Defaults to 'inf'.

    Returns:
        int: 0 if there is not error, otherwise -1.
    """
    if type(options) == setup:
        options = options.__get_dictionary()
    
    
    t1 = time.time()
    
    conf = reader.read_config_file(options['input'])

    if max_function_files == 'inf' or len(list(conf.keys())) < max_function_files:
        result = validate_bis(options, conf)
    else:
        conf2 = {}
        i = 0
        result = 0
        for k in conf.keys():
            if i == max_function_files:
                result += validate_bis(options, conf2)
                conf2 = {}
                i = 0
            conf2[k] = conf[k]
            i+=1
        result = -1 if result != 0 else 0

    if options['verbose']:
        print("Process duration: " + str(round(time.time()-t1, 2)) + "s")

    return result

"""
'absmax': [['float', 'float'], ['double', 'double'], ['std::int64_t', 'std::int64_t'], ['std::int32_t', 'std::int32_t'], 
           ['std::int16_t', 'std::int16_t'], ['std::int8_t', 'std::int8_t'], ['std::uint64_t', 'std::uint64_t'], ['std::uint32_t', 'std::uint32_t'], 
           ['std::uint16_t', 'std::uint16_t'], ['std::uint8_t', 'std::uint8_t'], ['std::uint64_t', 'std::uint64_t'], 
           ['std::uint32_t', 'std::uint32_t'], ['std::uint16_t', 'std::uint16_t'], ['std::uint8_t', 'std::uint8_t']]


{'absmax': [['float', 'float'], ['double', 'double'], ['std::int64_t', 'std::int64_t'], ['std::int32_t', 'std::int32_t'], ['std::int16_t', 'std::int16_t'], 
['std::int8_t', 'std::int8_t'], ['std::uint64_t', 'std::uint64_t'], ['std::uint32_t', 'std::uint32_t'], ['std::uint16_t', 'std::uint16_t'], 
['std::uint8_t', 'std::uint8_t'], ['std::uint64_t', 'std::uint64_t'], ['std::uint32_t', 'std::uint32_t'], ['std::uint16_t', 'std::uint16_t'], 
['std::uint8_t', 'std::uint8_t']]}
"""

if __name__ == '__main__':
    print(validate(input='all', log_file=True, raise_exception=True, keep_tmp=True))