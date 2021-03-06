#! /usr/bin/env python

import sys
import os
from multiprocessing import Process, freeze_support

if __name__ == '__main__':
    try:
        libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
        sys.path.insert(0, libdir)
    except:
        # probably running inside py2exe which doesn't set __file__
        pass

    import main

    if '-profile' in sys.argv:
        import profile

        profile.run('main.main()')
    else:
        freeze_support()
        main.main()
