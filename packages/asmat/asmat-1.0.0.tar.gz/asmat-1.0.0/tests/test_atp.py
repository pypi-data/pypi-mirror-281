import unittest
from test_utils import ignore_warnings
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/../src")
import atp
import files
import validation
import const

path = f"{os.path.dirname(__file__)}"

test_mismatch_1 = """{
    "function": "add",
    "asm": [
        {
            "type": [
                "float",
                "float"
            ],
            "instr": [
                "addps %xmm1,%xmm2"
            ]
        }
    ]
}"""

test_mismatch_2 = """{
    "function": "add",
    "asm": [
        {
            "type": [
                "float",
                "float"
            ],
            "instr": [
                "addpm %xmm1,%xmm0"
            ]
        }
    ]
}"""

test_mismatch_3 = """{
    "function": "max",
    "asm": [
        {
            "type": [
                "float",
                "float"
            ],
            "instr": [
                "maxps %xmm1,%xmm0"
            ]
        },
        {
            "type": [
                "double",
                "double"
            ],
            "instr": [
                "maxpd %xmm1,%xmm2"
            ]
        },
        {
            "type": [
                "int",
                "int"
            ],
            "instr": [
                "maxpd %xmm1,%xmm0"
            ]
        }
    ]
}"""

test_match_1 = """{
    "function": "add",
    "asm": [
        {
            "type": [
                "float",
                "float"
            ],
            "instr": [
                "addps %xmm1,%xmm0"
            ]
        }
    ]
}"""



class TestOptionToDict(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_equal_output(self):
        d = const.OPTIONS.copy()

        d['setup'] = "avx"
        test1 = atp.options_to_dict(["..", "-s", "avx"])
        self.assertEqual(test1, d)

        test2 = atp.options_to_dict(["..", "-s", "avx", "-d", "-l"])
        d['log'] = True
        d['deep'] = True
        self.assertEqual(test2, d)

        test3 = atp.options_to_dict(["..", "-s", "avx", "-d", "-l", '-t', '-g'])
        d['generate'] = True
        d["keep_tmp"] = True
        d['validate'] = False
        self.assertEqual(test3, d)

        test4 = atp.options_to_dict(["..", "-s", "avx", "-d", "-l", '-t', '-g', '--input', 'abs.json'])
        d['input'] = 'abs.json'
        self.assertEqual(test4, d)



    def test_input(self):
        d = const.OPTIONS.copy()
        
        test1 = atp.options_to_dict(["..", '--input', 'abs.json', '-l', '-v'])
        d['log'] = True
        d['verbose'] = True
        d['input'] = 'abs.json'

        self.assertEqual(test1, d)

        test2 = atp.options_to_dict(["..", '-l', '--input', 'abs.json', '-v'])
        d['log'] = True
        d['verbose'] = True
        d['input'] = 'abs.json'

        self.assertEqual(test2, d)

        test3 = atp.options_to_dict(["..", '-l', '-v', '--input', 'abs.json'])
        d['log'] = True
        d['verbose'] = True
        d['input'] = 'abs.json'

        self.assertEqual(test3, d)


    def test_error_invalid_option(self):
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', 's', 's'])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', ''])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', '-', 's'])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', '-', 't', 's', '-'])
        

    def test_invalid_input_file(self):
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', '--input'])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', '-input', 'abs.json'])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', 'abs.json', '--input'])
        with self.assertRaises(Exception):
            atp.options_to_dict(['..', '--input', '-t'])


class TestAtp(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @ignore_warnings
    def test_valid_references(self):
        files.build_reference_directories(f"{path}/atp")
        if os.path.exists(f"{path}/atp/gcc/sse/add.json"):
            file = open(f"{path}/atp/gcc/sse/add.json", 'w')
        else:
            file = open(f"{path}/atp/gcc/sse/add.json", 'x')
        file.write(test_match_1)
        file.close()

        d = const.OPTIONS.copy()
        d['arch'] = 'sse'
        d['validate'] = True
        d['input'] = "add.json"
        d['compiler'] = 'gcc'
        d['ref_path'] = f"{path}/atp"


        self.assertEqual(atp.main(d), 0)

        files.reset(folder=f'{path}/atp')

    """
    def test_unmatched_references(self):
        files.build_reference_directories(f"{const.root}/test/atp")
        if os.path.exists(f"{const.root}/test/atp/gcc/sse/add.json"):
            file = open(f"{const.root}/test/atp/gcc/sse/add.json", 'w')
        else:
            file = open(f"{const.root}/test/atp/gcc/sse/add.json", 'x')
        file.write(test_mismatch_1)
        file.close()
        
        d = const.OPTIONS.copy()
        d['validate'] = True
        d['compiler'] = "gcc"
        d['input'] = 'add.json'
        d['setup'] = 'sse'
        d['ref_path'] = f"{const.root}/test/atp"

        self.assertEqual(atp.main(d), -1)

        if os.path.exists(f"{const.root}/test/atp/gcc/sse/add.json"):
            file = open(f"{const.root}/test/atp/gcc/sse/add.json", 'w')
        else:
            file = open(f"{const.root}/test/atp/gcc/sse/add.json", 'x')
        file.write(test_mismatch_2)
        file.close()

        self.assertEqual(atp.main(d), -1)


        d['arch'] = 'sse3'
        d['input'] = "max.json"
        if os.path.exists(f"{const.root}/test/atp/gcc/sse4.2/max.json"):
            file = open(f"{const.root}/test/atp/gcc/sse4.2/max.json", 'w')
        else:
            file = open(f"{const.root}/test/atp/gcc/sse4.2/max.json", 'x')
        file.write(test_mismatch_3)
        file.close()

        self.assertEqual(atp.main(d), -1)

        const.OPTIONS['exception'] = True
        with self.assertRaises(validation.AssemblyMismatch):
            atp.main(d)
        
        files.reset(folder=f'{const.root}/test/atp')
    """

    @ignore_warnings
    def test_gen_and_valid(self):
        files.build_reference_directories(f"{path}/atp")

        d = const.OPTIONS.copy()
        d['ref_path'] = f"{path}/atp"
        d['deep'] = True
        d['generate'] = True

        atp.main(d)

        d['validate'] = True
        d['generate'] = False

        self.assertEqual(atp.main(d), 0)

        files.reset(folder=f'{path}/atp')




if __name__ == '__main__':
    unittest.main()