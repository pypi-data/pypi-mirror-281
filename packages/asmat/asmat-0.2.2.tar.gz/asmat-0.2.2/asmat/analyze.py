import asmat.instructions as instructions
import asmat.const as const
import asmat.reader as reader








def analyze_assembly(options:dict, function, compiler:str, cpu_ext:str, param):

    output_directory = options['output']
    deep = options['deep']
    verbose = options['verbose']
    conf = reader.read_config_file(options['input'])

    if output_directory == None:
        output_directory = f"{const.ref_path}"

    functions = []
    for k in conf.keys():
        for typ in conf[k]:
            functions.append((k, typ))

    instr = [i['instr'] for i in instructions.get_functions_instructions(options, functions)[compiler][cpu_ext][function] if i['type'] == param][0]

    print(instr)


if __name__ == '__main__':
    opt = const.OPTIONS.copy()
    opt['input'] = 'add.json'
    opt['compiler'] = 'g++'
    opt['setup'] = 'avx'
    analyze_assembly(opt, 'add', 'g++', 'avx', ['float', 'float'])

