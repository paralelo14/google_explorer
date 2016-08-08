"""
Usage:
    joomlaexp.py --file=<arg>
    joomlaexp.py --help
    joomlaexp.py --version

Options:
    -h --help                                Open help menu
    -v --version                             Show version

Required options:
    --file='arq'                             arq
"""

import os
import sys
import time

from docopt import docopt, DocoptExit

def main():
    arguments = docopt(__doc__, version="TWA Corp. Google Explorer - 2016")
    filename = arguments['--file']

    f = open(filename, 'r')
    for target in f.readlines():
        os.system(target.rstrip())

    cmd = 'rm -rf {0}'.format(filename)
    os.system(cmd)

if __name__ == '__main__':
    main()