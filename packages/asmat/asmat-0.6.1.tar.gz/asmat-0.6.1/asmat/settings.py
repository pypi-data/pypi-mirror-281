import json
import os
import asmat.reader as reader
import asmat.const as const
from asmat.reader import get_groups



def get_setup(entry:str):
    """Returns simd extensions with their corresponding compiler flag. If `entry` is not found in the settings file\
    it is considered as a custom flag.

    Args:
        entry (str): Name of the simd extension to search.

    Returns:
        dict: Dictionary associating entry with its corresponding flag.
    """
    
    settings = reader.load_json(const.settings)
    settings = json.loads(settings)
    if entry == 'all':
        return settings['setup']
    else:
        if entry in settings['setup'].keys():
            return {entry : settings['setup'][entry]}
        else:
            return {entry : entry}
    

def get_flags():
    settings = reader.load_json(const.settings)
    settings = json.loads(settings)
    return settings['flags']


def get_type_wrapper():
    settings = reader.load_json(const.settings)
    settings = json.loads(settings)
    return settings['type_wrapper']


def get_compiler(entry:str):
    """Returns compilers with there corresponding name in the system. If `entry` is found in settings file\
    the corresponding path is returned as the value in the dictionary. Otherwise `entry` is defined as the value and\
    the key is the basename.

    Args:
        entry (str): Name of the compiler.

    Returns:
        dict: The compiler's name associated with the path to execute it.
    """

    settings = reader.load_json(const.settings)
    settings = json.loads(settings)
    if entry == 'all':
        return settings['compilers']
    else:
        if entry in settings['compilers'].keys():
            return {entry : settings['compilers'][entry]}
        else:
            return {os.path.basename(entry) : entry}





def get_target(options:dict):
    """Returns all necessary information about the target. The returned dictionary contains information about:
    - compilers
    - simd extensions
    - functions
    - input
    - type_wrapper
    - output

    Args:
        options (dict): Dictionary describing user query. The structure of the dictionary is stored in `const.OPTIONS`.

    Returns:
        dict: Information about the target.
    """

    d = {}
    if options['flags'] != []:
        if options['compiler'] == None or options['compiler'] == 'all':
            d['compiler'] = get_compiler('all')
        else:
            c = get_compiler(options['compiler'])
            if c == {}:
                d['compiler'] = options['compiler']
            else:
                d['compiler'] = c
        d['setup'] = { 'custom' : options['flags'] }
        
    else:
        if options['compiler'] == None or options['compiler'] == 'all':
            d['compiler'] = get_compiler('all')
        else:
            c = get_compiler(options['compiler'])
            if c == {}:
                d['compiler'] = options['compiler']
            else:
                d['compiler'] = c
        if options['setup'] == None or options['compiler'] == 'all':
            d['setup'] = get_setup('all')
        else:
            d['setup'] = get_setup(options['setup'])

    if input == 'all':
        d['input'] = reader.read_config_file('all')
    else:
        d['input'] = reader.read_config_file(options['input'])
    
    d['twrapper'] = get_type_wrapper()

    d['output'] = options['output']
    return d
        
            





if __name__ == '__main__':
    print(get_groups('abs'))