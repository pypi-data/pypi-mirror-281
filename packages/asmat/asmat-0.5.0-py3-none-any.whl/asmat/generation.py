import json
import asmat.instructions as instructions
import asmat.const as const
import asmat.reader as reader
import os
import time
from asmat.option import setup



def save_json(destination_path:str, text:str):
    """Save string in a file.

    Args:
        destination_path (str): Path to save file.
        text (str): File content.

    Raises:
        Exception: Raised when error occured while writing the file.
    """
    if not os.path.exists(destination_path):
        try:
            f = open(destination_path, 'x')
            f.write(text)
            f.close()
        except Exception as e:
            raise Exception(f"Error while writing {destination_path} : {e}")
    else:
        try:
            f = open(destination_path, 'w')
            f.write(text)
            f.close()
        except Exception as e:
            raise Exception(f"Error while writing {destination_path} : {e}")





def generate_bis(options:dict, conf:dict) -> int:
    """Generate and store assembly code

    Args:
        options (dict): Dictionary describing user query. The structure of the dictionary is stored in `const.OPTIONS`.
        conf (dict): Configuration with all information about compilation targets.

    Returns:
        int: 0
    """

    output_directory = options['output']
    deep = options['deep']
    verbose = options['verbose']

    if output_directory == None:
        output_directory = f"{const.ref_path}"

    functions = []
    for k in conf.keys():
        for typ in conf[k]:
            functions.append((k, typ))

    functions_assembly = instructions.get_functions_instructions(options, functions)

    for comp in functions_assembly.keys():
        for arch in functions_assembly[comp].keys():
            for f in functions_assembly[comp][arch].keys():
                try:
                    os.makedirs(f"{output_directory}/{comp}/{arch}")
                except FileExistsError:
                    pass

                if not os.path.exists(f"{output_directory}/{comp}/{arch}/{f}.json"):
                    file = open(f"{output_directory}/{comp}/{arch}/{f}.json", 'x')
                    file.close()
                    dict_json = { "function" : f, "asm" : functions_assembly[comp][arch][f] }
                    update_json = json.dumps(dict_json, indent=4)
                    save_json(f"{output_directory}/{comp}/{arch}/{f}.json", update_json)
                elif reader.load_json(f"{output_directory}/{comp}/{arch}/{f}.json") == '' or reader.load_json(f"{output_directory}/{comp}/{arch}/{f}.json") == '{}' or deep:
                    dict_json = { "function" : f, "asm" : functions_assembly[comp][arch][f] }
                    
                    update_json = json.dumps(dict_json, indent=4)
                    save_json(f"{output_directory}/{comp}/{arch}/{f}.json", update_json)

    if verbose:
        print(f"Operation finished : functions saved")

    return 0
    




def generate(options: dict | setup, max_function_files='inf') -> int:
    """Auxiliary function for generation. This function limits the function per file for compilation.

    Args:
        options (dict): Dictionary describing user query. The structure of the dictionary is stored in `const.OPTIONS`
        max_function_files (str, optional): The maximum number of function in a cpp file. A function is one config file (it can generate more than one if there are several\
              parameters configuration). Defaults to 'inf'.

    Returns:
        int: 0
    """

    if type(options) == setup:
        options = options.__get_dictionary()

    t1 = time.time()


    conf = reader.read_config_file(options['input'])

    if max_function_files == 'inf' or len(list(conf.keys())) < max_function_files:
        result = generate_bis(options, conf)
    else:
        conf2 = {}
        i = 0
        result = 0
        for k in conf.keys():
            if i == max_function_files:
                result += generate_bis(options, conf2)
                conf2 = {}
                i = 0
            conf2[k] = conf[k]
            i+=1
        result = -1 if result != 0 else 0

    if options['verbose']:
        print("Process duration: " + str(round(time.time()-t1, 2)) + "s")

    return result


if __name__ == '__main__':
    pass