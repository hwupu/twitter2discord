import sys

if sys.version_info.major < 3:
    print('\033[1;31mNeeds Python3 to run.\033[m')
    exit(1)

from . import handler
handler.main()
