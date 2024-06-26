import asmat
import asmat.option as opt

s = opt.setup()
s.verbose = True

asmat.build_dependencies() # Build files

asmat.generate(s)

asmat.validate(s)