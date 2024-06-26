import os
#import sys
import  asmat.analysis.analysis_output as analysis_output
#sys.path.append(f"{os.path.dirname(__file__)}/..")
import asmat.instructions as instructions
import asmat.const as const
import asmat.reader as reader



def analyze(options:dict, compiler:str, cpu_ext:str):

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
            param = ""
            for p in range(0, len(j['type'])):
                if p == len(j['type'])-1 or len(j['type']) == 0:
                    param += j['type'][p]
                else:
                    param += j['type'][p] + ', '

            index.append((f"{i}({param})", j['instr']))

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

