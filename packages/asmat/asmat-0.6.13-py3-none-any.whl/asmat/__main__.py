from asmat.atp import options_to_dict, main
import sys

argv = sys.argv
    
options = options_to_dict(argv)
main(options)