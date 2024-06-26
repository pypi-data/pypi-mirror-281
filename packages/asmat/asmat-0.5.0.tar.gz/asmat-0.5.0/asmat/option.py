import asmat.const as const


class setup:

    def __init__(self) -> None:
        self.log = False
        self.deep = False
        self.input = 'all'
        self.keep_tmp = False
        self.exception = False
        self.verbose = False
        self.disassembler = "objdump"
        self.instruction_comparison = False
        self.flags = []
        self.setup = None
        self.compiler = None
        self.output = f"{const.root}/ref"
        self.limit_file = 'inf'
        self.nbprocess = 0
        self.headers = []

    def __get_dictionary(self):
        d = {
            "validate" : False,
            "log" : self.log,
            "deep" : self.deep,
            "input" : self.input,
            "keep_tmp" : self.keep_tmp,
            "generate" : False,
            "exception" : self.exception,
            "verbose" : self.verbose,
            "disassembler" : self.disassembler,
            "instruction_comparison" : self.instruction_comparison,
            "flags" : self.flags,
            "setup" : self.setup,
            "compiler" : self.compiler,
            "output" : self.output,
            "limit_per_file" : self.limit_file,
            "nbprocess" : self.nbprocess,
            "headers" : self.headers
        }
        return d
    
    def help(self):
        print("Options:")
        print("\t**log** : Boolean. True to generate log file if an error occurs. Defaults to False.")
        print("\t**deep** : Boolean. True to replace files previously referenced. Defaults to False.")
        print("\t**input** : String. Config files to take as input. Defaults to 'all'.")
        print("\t**keep_tmp** : Boolean. True to keep temporary files. Defaults to False.")
        print("\t**exception** : Boolean. True to raise exception when an error occurs. Defaults to False.")
        print("\t**verbose** : Boolean. True to print information in command line. Defaults to False.")
        print("\t**disassembler** : String. Defines the disassembly mode. Correct values are 'objdump' and 'standard'. Defaults to 'objdump'")
        print("\t**instruction_comparison** : Boolean. True to check instructions and ignore parameters. Defaults to False.")
        print("\t**flags** : string list. List of compilation options without '-'. Defaults to []")
        


if __name__ == '__main__':
    s = setup()
    s.help()