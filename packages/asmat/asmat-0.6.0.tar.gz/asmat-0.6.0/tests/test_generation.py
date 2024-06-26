import unittest
import os
import sys
from test_utils import ignore_warnings
sys.path.append(f"{os.path.dirname(__file__)}/../src")
import generation
import files
import settings
import const

path = f"{os.path.dirname(__file__)}"



class TestUpdateGeneration(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @ignore_warnings
    def test_output_files(self):

        os.system(f"rm -rf {path}/generation/*")
        
        d = const.OPTIONS.copy()
        d['output'] = f"{path}/generation/"
        generation.generate(d)

        sett = settings.get_target(d)
        for c in sett['compiler'].keys():
            for a in sett['setup'].keys():
                for f in os.listdir(f"{const.root}/config"):
                    self.assertTrue( os.path.exists( f"{path}/generation/{c}/{a}/{f}" ) )
        
        files.reset(f"{path}/generation")
                                        
                                        

if __name__ == '__main__':
    unittest.main()