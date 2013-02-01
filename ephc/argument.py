import optparse



# http://docs.python.org/2/library/optparse.html#optparse-extending-optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--timeout", dest="timeout", type=int, default=60,
                      help="Time in seconds to time out a connection")
                      
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="Show health check status as you go")
                      
    parser.add_option("-f", "--format", dest="format",
                      choices=('bashmon', 'json'),
                      help="Specify an optional output format")
                      
    #parser.add_option("-s", "--sections", dest="sections", )
                      
                      
    (options, args) = parser.parse_args()
    
    return options
    
    
args = get_arguments()