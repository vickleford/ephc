import os

import yaml


config_locations = [ '/etc/ephc/config.yaml', '~/.config/ephc/config.yaml' ]


if 'EPHC_CONFIG' in os.environ:
    config_locations.append(os.environ['EPHC_CONFIG'])

for filename in config_locations:
    
    # take home dir shorthand
    filename = os.path.expanduser(filename)
    
    try:    
        with open(filename) as f:
            config = yaml.load(f)
            print "Loaded config file %s" % filename
            break
    except IOError, ioe:
        if ioe.errno == 2:
            # np, try the next file
            print "Could not load %s" % filename

