import sys

from core.__main__ import main

if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    sys.exit(main())
