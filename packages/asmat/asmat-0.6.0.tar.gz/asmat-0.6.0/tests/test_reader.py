import unittest
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/../src")
import reader
import const
import numpy


path = f"{os.path.dirname(__file__)}"


class TestReader(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_reader_reference_file(self):
        self.assertEqual(reader.load_json(f"{path}/reader/test1.json"), '{}')

        with self.assertRaises(Exception):
            reader.load_json('.')
        with self.assertRaises(FileNotFoundError):
            reader.load_json(f'{path}/reader/test.json')

        self.assertNotEqual(reader.load_json(f"{path}/reader/test2.json"), "{}")


    def test_keytypes_to_types(self):
        t1 = reader.keytypes_to_types([['float', 'float'], ['int', 'int'], ['double', 'double']])
        self.assertEqual(t1, [['float', 'float'], ['int', 'int'], ['double', 'double']])


        t2 = reader.keytypes_to_types([['arithmetic']])
        self.assertEqual(t2, [[i] for i in const.ARITHMETIC])

        t3 = reader.keytypes_to_types([['arithmetic', 'arithmetic']])
        self.assertEqual(t3, [[i, i] for i in const.ARITHMETIC])

        t4 = reader.keytypes_to_types([['arithmetic', 'arithmetic', 'float']])
        self.assertEqual(t4, [[i, i, 'float'] for i in const.ARITHMETIC])

        t5 = reader.keytypes_to_types([['double', 'arithmetic', 'arithmetic', 'float']])
        self.assertEqual(t5, [['double', i, i, 'float'] for i in const.ARITHMETIC])

        t6 = reader.keytypes_to_types([['double', 'arithmetic', 'arithmetic', 'float'], ['arithmetic', 'float']])
        self.assertEqual(t6, [['double', i, i, 'float'] for i in const.ARITHMETIC] + [[i, 'float'] for i in const.ARITHMETIC])

        t7 = reader.keytypes_to_types([[], ['double', 'arithmetic', 'arithmetic', 'float'], [], ['arithmetic', 'float'], []])
        self.assertEqual(t7, [['double', i, i, 'float'] for i in const.ARITHMETIC] + [[i, 'float'] for i in const.ARITHMETIC])

        t8 = reader.keytypes_to_types([['real', 'arithmetic']])
        for i in t8:
            self.assertTrue(i[0] in const.REAL and i[1] in const.ARITHMETIC)
        self.assertEqual(len(t8), len(const.ARITHMETIC) + len(const.REAL))

        t9 = reader.keytypes_to_types([['real', 'arithmetic', 'arithmetic', 'integer']])
        for i in t9:
            self.assertTrue(i[0] in const.REAL and i[1] in const.ARITHMETIC and i[2] in const.ARITHMETIC and i[3] in const.INTEGER)
        self.assertEqual(len(t9), len(const.ARITHMETIC) + len(const.REAL) + len(const.INTEGER))

        fst = [i[0] for i in t9]
        for i in const.REAL:
            self.assertTrue(i in fst)
        for i in fst:
            self.assertTrue( i in const.REAL )


        self.assertTrue( numpy.array(t1).ndim == 2 )
        self.assertTrue( numpy.array(t2).ndim == 2 )
        self.assertTrue( numpy.array(t3).ndim == 2 ) 
        self.assertTrue( numpy.array(t4).ndim == 2 )
        self.assertTrue( numpy.array(t5).ndim == 2 )
        self.assertTrue( numpy.array(t8).ndim == 2 )
        self.assertTrue( numpy.array(t9).ndim == 2 )

if __name__ == '__main__':
    unittest.main()