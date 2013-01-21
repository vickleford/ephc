import os

import yaml


config_locations = [ '/etc/ephc/config.yaml', '~/.config/ephc/config.yaml' ]

if 'EPHC_CONFIG' in os.environ:
    config_locations.append(os.environ['EPHC_CONFIG'])

for filename in config_locations:    
    try:    
        with open(filename) as f:
            config = yaml.load(f)
            break
        except IOError, ioe:
            if ioe.errno == 2:
                # np, try the next file
                break