import sys

if sys.version_info.major < 3:
    print('\033[1;31mNeeds Python3 to run.\033[m')
    exit(1)

from . import database
from . import handler

try:
    database.connect()
    handler.main()
except KeyboardInterrupt:
    print('\033[1;30mKeyboardInterrupt\033[m')
except EOFError:
    print('\033[1;30mEOFError\033[m')
finally:
    database.close()
