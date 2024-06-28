import unittest
import sys
from test_utils import ignore_warnings
import os
sys.path.append(f"{os.path.dirname(__file__)}/../src")
from instructions import *
import const

path = f"{os.path.dirname(__file__)}"

class TestGenerateFunction(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        clear_tmp()
    

    def test_valid_file_output(self):
        clear_tmp()

        c1 = generate_function("test1", [], functionId=0)
        t1 = ("test1_0", """auto func_test1_0() {
    return eve::test1();
}
""")

        c2 = generate_function("test2", ['eve::wide<float>'], functionId=1)
        t2 = ("test2_1", """auto func_test2_1(eve::wide<float> a0) {
    return eve::test2(a0);
}
""")
        c3 = generate_function("test3", ['eve::wide<float>', 'eve::wide<int>', 'eve::wide<double>'], functionId=2)
        t3 = ("test3_2", """auto func_test3_2(eve::wide<float> a0, eve::wide<int> a1, eve::wide<double> a2) {
    return eve::test3(a0, a1, a2);
}
""")

        c4 = generate_function("test4", ['eve::wide<int>', 'eve::wide<int>'], functionId=3)
        t4 = ("test4_3", """auto func_test4_3(eve::wide<int> a0, eve::wide<int> a1) {
    return eve::test4(a0, a1);
}
""")
        
        c5 = generate_function("", [], functionId=4)
        t5 = ("_4", """auto func__4() {
    return eve::();
}
""")
        self.assertEqual(c1, t1)
        self.assertEqual(c2, t2)
        self.assertEqual(c3, t3)
        self.assertEqual(c4, t4)
        self.assertEqual(c5, t5)


class TestExtractInstructions(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.asm = """00000000000000d0 <func_dist_8(eve::avx512_abi_v0::wide<float, eve::fixed<16l> >, eve::avx512_abi_v0::wide<float, eve::fixed<16l> >)>:
  d0:	f3 0f 1e fa          	endbr64 
  d4:	4c 8d 54 24 08       	lea    0x8(%rsp),%r10
  d9:	48 83 e4 c0          	and    $0xffffffffffffffc0,%rsp
  dd:	41 ff 72 f8          	push   -0x8(%r10)
  e1:	55                   	push   %rbp
  e2:	48 89 e5             	mov    %rsp,%rbp
  e5:	41 52                	push   %r10
  e7:	48 83 ec 28          	sub    $0x28,%rsp
  eb:	e8 30 ff ff ff       	call   20 <eve::avx512_abi_v0::wide<float, eve::fixed<16l> > eve::detail::dist_<eve::avx512_abi_v0::wide<float, eve::fixed<16l> >, eve::options<rbr::settings<rbr::option<eve::detail::condition_key_t, eve::ignore_none_> > > >(eve::detail::adl_helper_t const&, eve::cpu_ const&, eve::options<rbr::settings<rbr::option<eve::detail::condition_key_t, eve::ignore_none_> > > const&, eve::avx512_abi_v0::wide<float, eve::fixed<16l> >, eve::avx512_abi_v0::wide<float, eve::fixed<16l> >) [clone .isra.0]>
  f0:	4c 8b 55 f8          	mov    -0x8(%rbp),%r10
  f4:	c9                   	leave  
  f5:	49 8d 62 f8          	lea    -0x8(%r10),%rsp
  f9:	c3                   	ret    
  fa:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

    0000000000000130 <func_add_10(eve::avx512_abi_v0::wide<float, eve::fixed<16l> >, eve::avx512_abi_v0::wide<float, eve::fixed<16l> >)>:
 130:	f3 0f 1e fa          	endbr64 
 134:	62 f1 74 48 58 c0    	vaddps %zmm0,%zmm1,%zmm0
 13a:	c3                   	ret    
 13b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
"""

    @ignore_warnings
    def test_valid_call(self):        
        t1 = extract_instructions('dist', ["float", "float"], {function_extended_name('dist', ["float", "float"]) : "dist_8"}, self.asm)
        t2 = extract_instructions('add', ["signed char", "signed char"], {function_extended_name('add', ["signed char", "signed char"]) : "add_10"}, self.asm)

        self.assertTrue( t1 == ['lea 0x8(%rsp),%r10', 'and $0xffffffffffffffc0,%rsp', 'push -0x8(%r10)', 'push %rbp', 'mov %rsp,%rbp', 'push %r10', 'sub $0x28,%rsp', 'call 20', 'mov -0x8(%rbp),%r10', 'leave', 'lea -0x8(%r10),%rsp'] )
        self.assertTrue( t2 == ['vaddps %zmm0,%zmm1,%zmm0'] )

        with self.assertRaises(Exception):
            extract_instructions('add', ["signed char"], {function_extended_name('add', ["signed char", "signed char"]) : "add_10"}, self.asm)
        with self.assertRaises(Exception):
            extract_instructions('add_10', ["signed char", "signed char"], {function_extended_name('add', ["signed char", "signed char"]) : "add_10"}, self.asm)
        with self.assertRaises(Exception):
            extract_instructions('add', ["signed char", "signed char", "signed char"], {function_extended_name('add', ["signed char", "signed char"]) : "add_10"}, self.asm)
        
        
    @ignore_warnings
    def test_func_not_found_exception(self):
        with self.assertRaises(Exception):
            extract_instructions('00', self.asm)



class TestGetFunctionInstructions(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.opt = const.OPTIONS.copy()
        self.opt['compiler'] = "gcc"
        self.opt['setup'] = "sse"
        self.opt['input'] = "all"
        self.opt["output"] = f"{path}/output"


    @ignore_warnings
    def test_valid_entry(self):
        
        t1 = get_functions_instructions(self.opt, [('add', ['int', 'int']), ('abs', ['float'])])

        self.assertEqual(list(t1.keys()), ['gcc'])
        self.assertEqual(list(t1['gcc'].keys()), ['sse'])
        self.assertEqual(list(t1['gcc']['sse'].keys()), ['add', 'abs'])

    @ignore_warnings
    def test_limit_case(self):
        t1 = get_functions_instructions(self.opt, [])

        self.assertEqual(list(t1.keys()), ['gcc'])
        self.assertEqual(list(t1['gcc'].keys()), ['sse'])
        
        for i in t1.keys():
            for j in t1[i].keys():
                self.assertEqual(t1[i][j], {})


if __name__ == '__main__':
    unittest.main()