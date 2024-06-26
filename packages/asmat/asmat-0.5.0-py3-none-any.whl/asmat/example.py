import asmat

asmat.build_dependencies() # Build files

opt = asmat.setup
opt['verbose'] = True

asmat.generate(opt)

asmat.validate(opt)