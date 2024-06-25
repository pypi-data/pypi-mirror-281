import os
import json
import asmat.const as const
import random

## This file aims to read json files and extract information from them

def load_json(file_name:str, create_if_not_found=False):
    """Returns json file contents as str

    Args:
        file_name (str): The contents of the file
        create_if_not_found (bool, optional): If True the file is created if it doesn't exist. If False it raises an error if the file doesn't exist. Defaults to False.

    Raises:
        FileNotFoundError: If the file is not found and create_if_not_found is False
        Exception: Other errors

    Returns:
        str: The content of the file
    """

    try:
        f = open(file_name)
        t = f.read()
        if t == '':
            t = '{}'
        f.close()
        return t
    except FileNotFoundError:
        if create_if_not_found:
            f = open(file_name, 'x')
            f.write("{}")
            f.close()
            return "{}"
        else:
            raise FileNotFoundError(f"File {file_name} not found")
    except Exception as e:
        raise Exception(f"Error while loading {file_name} : {e}")



def keytypes_to_types(types:list):
    """Converts key types `arithmetic`, `real`, `unsigned`, `integer` to the corresponding cpp types

    Args:
        types (list): 2D list extract from json config files

    Returns:
        list: 2D list with key types replaced by cpp files
    """

    random.seed = 42

    valid_types = []
    
    for t in types:
        if t == []:
            continue

        if 'arithmetic' in t or 'integer' in t or 'real' in t or 'unsigned' in t:
            if 'arithmetic' in t:
                for a in const.ARITHMETIC:
                    tmp = [a if i == 'arithmetic' else i for i in t]
                    tmp = [const.REAL[random.randint(0, len(const.REAL)-1)] if i == 'real' else i for i in tmp]
                    tmp = [const.INTEGER[random.randint(0, len(const.INTEGER)-1)] if i == 'integer' else i for i in tmp]
                    tmp = [const.UNSIGNED_INTEGER[random.randint(0, len(const.UNSIGNED_INTEGER)-1)] if i == 'unsigned_integer' else i for i in tmp]
                    tmp = [const.SIGNED[random.randint(0, len(const.SIGNED)-1)] if i == 'signed' else i for i in tmp]
                    tmp = [const.SIGNED_INTEGER[random.randint(0, len(const.SIGNED_INTEGER)-1)] if i == 'signed_integer' else i for i in tmp]
                    valid_types.append(tmp)
            if 'integer' in t:
                for a in const.INTEGER:
                    tmp = [const.ARITHMETIC[random.randint(0, len(const.ARITHMETIC)-1)] if i == 'arithmetic' else i for i in t]
                    tmp = [const.REAL[random.randint(0, len(const.REAL)-1)] if i == 'real' else i for i in tmp]
                    tmp = [a if i == 'integer' else i for i in tmp]
                    tmp = [const.UNSIGNED_INTEGER[random.randint(0, len(const.UNSIGNED_INTEGER)-1)] if i == 'unsigned_integer' else i for i in tmp]
                    tmp = [const.SIGNED[random.randint(0, len(const.SIGNED)-1)] if i == 'signed' else i for i in tmp]
                    tmp = [const.SIGNED_INTEGER[random.randint(0, len(const.SIGNED_INTEGER)-1)] if i == 'signed_integer' else i for i in tmp]
                    valid_types.append(tmp)
            if 'real' in t:
                for a in const.REAL:
                    tmp = [const.ARITHMETIC[random.randint(0, len(const.ARITHMETIC)-1)] if i == 'arithmetic' else i for i in t]
                    tmp = [a if i == 'real' else i for i in tmp]
                    tmp = [const.INTEGER[random.randint(0, len(const.INTEGER)-1)] if i == 'integer' else i for i in tmp]
                    tmp = [const.UNSIGNED_INTEGER[random.randint(0, len(const.UNSIGNED_INTEGER)-1)] if i == 'unsigned_integer' else i for i in tmp]
                    tmp = [const.SIGNED[random.randint(0, len(const.SIGNED)-1)] if i == 'signed' else i for i in tmp]
                    tmp = [const.SIGNED_INTEGER[random.randint(0, len(const.SIGNED_INTEGER)-1)] if i == 'signed_integer' else i for i in tmp]
                    valid_types.append(tmp)
            if 'unsigned_integer' in t:
                for a in const.UNSIGNED_INTEGER:
                    tmp = [const.ARITHMETIC[random.randint(0, len(const.ARITHMETIC)-1)] if i == 'arithmetic' else i for i in t]
                    tmp = [const.REAL[random.randint(0, len(const.REAL)-1)] if i == 'real' else i for i in tmp]
                    tmp = [const.INTEGER[random.randint(0, len(const.INTEGER)-1)] if i == 'integer' else i for i in tmp]
                    tmp = [const.SIGNED[random.randint(0, len(const.SIGNED)-1)] if i == 'signed' else i for i in tmp]
                    tmp = [const.SIGNED_INTEGER[random.randint(0, len(const.SIGNED_INTEGER)-1)] if i == 'signed_integer' else i for i in tmp]
                    tmp = [a if i == 'unsigned_integer' else i for i in tmp]
                    valid_types.append(tmp)
            if 'signed_integer' in t:
                for a in const.SIGNED_INTEGER:
                    tmp = [const.ARITHMETIC[random.randint(0, len(const.ARITHMETIC)-1)] if i == 'arithmetic' else i for i in t]
                    tmp = [const.REAL[random.randint(0, len(const.REAL)-1)] if i == 'real' else i for i in tmp]
                    tmp = [const.INTEGER[random.randint(0, len(const.INTEGER)-1)] if i == 'integer' else i for i in tmp]
                    tmp = [const.UNSIGNED_INTEGER[random.randint(0, len(const.UNSIGNED_INTEGER)-1)] if i == 'unsigned_integer' else i for i in tmp]
                    tmp = [const.SIGNED[random.randint(0, len(const.SIGNED)-1)] if i == 'signed' else i for i in tmp]
                    tmp = [a if i == 'signed_integer' else i for i in tmp]
                    valid_types.append(tmp)
            if 'signed' in t:
                for a in const.SIGNED:
                    tmp = [const.ARITHMETIC[random.randint(0, len(const.ARITHMETIC)-1)] if i == 'arithmetic' else i for i in t]
                    tmp = [const.REAL[random.randint(0, len(const.REAL)-1)] if i == 'real' else i for i in tmp]
                    tmp = [const.INTEGER[random.randint(0, len(const.INTEGER)-1)] if i == 'integer' else i for i in tmp]
                    tmp = [const.UNSIGNED_INTEGER[random.randint(0, len(const.UNSIGNED_INTEGER)-1)] if i == 'unsigned_integer' else i for i in tmp]
                    tmp = [const.SIGNED_INTEGER[random.randint(0, len(const.SIGNED_INTEGER)-1)] if i == 'signed_integer' else i for i in tmp]
                    tmp = [a if i == 'signed' else i for i in tmp]
        else:
            valid_types.append(t)
                
    return valid_types



def get_groups(entry:str):
    """Returns list of config file if the group is found. Otherwise it returns an empty list.

    Args:
        entry (str): The name of the group.

    Returns:
        list: List of config files.
    """

    settings = load_json(const.settings)
    settings = json.loads(settings)
    g = [i for i in settings['groups'] if i['name'] == entry]
    if len(g) > 0 :
        return g[0]['files']
    else:
        return []


def read_headers():
    settings = load_json(const.settings)
    settings = json.loads(settings)
    return settings['headers']
    



def read_config_file(file_name='all'):
    """Reads config files stored in `config` directory. Files are returned as dictionary.

    Args:
        file_name (str, optional): Files we want to read. If all, it reads all the files in `config` directory. Defaults to 'all'.

    Raises:
        Exception: If the file in argument doesn't exist.

    Returns:
        dict: Dictionary with functions names and parameters types.
    """

    if file_name == 'all':
        d = {}
        for f in os.listdir(f"{const.root}/config"):
            txt = load_json(f"{const.root}/config/{f}")
            function = json.loads(txt)
            d[function['function']] = keytypes_to_types(function['parameters'])
        return d
    else:
        g = get_groups(file_name)
        if g != []:
            file_name = g
        else:
            file_name = [file_name]

        d = {}
        for n in file_name:
            if os.path.exists(f"{const.root}/config/{n}"):
                txt = load_json(f"{const.root}/config/{n}")
                function = json.loads(txt)
                d[function['function']] = keytypes_to_types(function['parameters'])
            elif os.path.exists(n):
                txt = load_json(n)
                function = json.loads(txt)
                d[function['function']] = keytypes_to_types(function['parameters'])
            else:
                raise Exception(f"Configuration file {n} not found.")
        return d
        





def read_reference_files(file_name:str, path="test/asm/ref"):
    """Reads a reference file and returns a dictionary. The file is read for every compilers and architectures

    Args:
        file_name (str): The name of the file to read (not the path).
        path (str, optional): The path of the reference folder. Defaults to "test/asm/ref".

    Returns:
        dict: Dictionary containing assembly program for every compiler and architecture.
    """
    references = {}
    for i in os.listdir(path):
        references[i] = {}
        for j in os.listdir(f"{path}/{i}"):
            references[i][j] = {}
            if file_name == 'all':
                for k in os.listdir(f"{path}/{i}/{j}"):
                    d = json.loads(load_json(f"{path}/{i}/{j}/{k}"))
                    references[i][j][d['function']] = d['asm']
            else:
                g = get_groups(file_name)

                if g != []:
                    names = g
                else:
                    names = [file_name]
                for k in names:
                    try:
                        d = json.loads(load_json(f"{path}/{i}/{j}/{k}"))
                        references[i][j][d['function']] = d['asm']
                    except FileNotFoundError:
                        print(f"File {path}/{i}/{j}/{k} not found")

    return references



if __name__ == '__main__':
    pass
    #print(read_reference_files('abs'))