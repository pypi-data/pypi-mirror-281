import os
if __name__ == "__main__":
    import sys
    sys.path.append("/home/erwan/eve/test/asm/src")

import  asmat.analysis.analysis_output as analysis_output

import asmat.instructions as instructions
import asmat.const as const
import asmat.reader as reader
from asmat.option import setup



def analyze(options:dict | setup, compiler:str=None, cpu_ext:str=None):
    """Analyzes assembly code of c++ functions. Gives a report in html format (in `/output` directory).

    Args:
        options (dict | setup): Setup object or dictionary containing user options.
        compiler (str, optional): The compiler to analyze. Defaults to None.
        cpu_ext (str, optional): The cpu extension to analyze. Defaults to None.

    Raises:
        Exception: If compiler or cpu_ext are not valid.
    """

    if compiler == None or cpu_ext == None:
        raise Exception("Missing compiler and cpu options for analysis.")

    if type(options) == setup:
        options = options.get_dictionary()

    output_directory = options['output']
    conf = reader.read_config_file(options['input'])

    if output_directory == None:
        output_directory = f"{const.ref_path}"

    functions = []
    for k in conf.keys():
        for typ in conf[k]:
            functions.append((k, typ))

    instr = instructions.get_functions_instructions(options, functions)[compiler][cpu_ext]

    index = []

    functions = sorted( list(instr.keys()) )
    for i in functions:
        for j in instr[i]:
            index.append((i, j['type'], j['instr']))

    if not os.path.exists(f"{const.root}/output"):
        os.mkdir(f"{const.root}/output")
    if not os.path.exists(f"{const.root}/output/pages"):
        os.mkdir(f"{const.root}/output/pages")
    
    analysis_output.generate_index(index)




if __name__ == '__main__':
    opt = const.OPTIONS.copy()
    opt['input'] = 'all'
    opt['compiler'] = 'g++'
    opt['setup'] = 'avx'
    analyze(opt, 'g++', 'avx')

