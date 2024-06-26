import os
import asmat.const as const


default_settings = """{
    "compilers":
        {
            // "gcc": "g++" // Example
        },
    "setup":
        {
            // "sse": "-msse" // Example
        }, 
    "groups": [
        /*
            Example
        {
            "name": "myGroup",
            "files": [
                "filename.json"
            ]
        }
        */
    ],
    "headers": [
        // C++ headers
    ],
    "flags": [
        // "-std=c++20" // Example
    ],
    "type_wrapper": ""
}"""




def build_dependencies(replace=False):
    if not os.path.exists(f"{const.root}/ref"):
        os.mkdir(f"{const.root}/ref")
    elif replace:
        os.remove(f"{const.root}/ref")
        os.mkdir(f"{const.root}/ref")

    if not os.path.exists(f"{const.root}/settings.json"):
        f = open(f"{const.root}/settings.json", 'x')
        f.write(default_settings)
        f.close()
        
    elif replace:
        f = open(f"{const.root}/settings.json", 'w')
        f.write(default_settings)
        f.close()

    if not os.path.exists(f"{const.root}/config"):
        os.mkdir(f"{const.root}/config")



def build_reference_directories(folder=f'{const.root}/ref'):
    """Builds directories for reference.

    Args:
        folder (str, optional): Path of the reference directory to build subdirectories. Defaults to 'test/asm/ref'.
    """

    if not os.path.exists(folder):
        os.mkdir(f"{folder}")

    for c in const.COMPILER:
        if not os.path.exists(f"{folder}/{c}"):
            os.mkdir(f"{folder}/{c}")

        for a in const.ARCH:
            if not os.path.exists(f"{folder}/{c}/{a}"):
                os.mkdir(f"{folder}/{c}/{a}")


def reset(folder=f'{const.root}/ref'):
    """Clear directory

    Args:
        folder (str, optional): Path of the directory. Defaults to 'test/asm/ref'.
    """
    os.system(f"rm -rf {folder}/*")



if __name__ == '__main__':
    pass
    #build_reference_directories()