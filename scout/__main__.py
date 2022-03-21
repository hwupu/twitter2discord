import sys

if sys.version_info.major < 3:
    print('\033[1;31mNeeds Python3 to run.\033[m')
    exit(1)

from . import initializer
from . import handler

try:
    config = initializer.get_config()
    conn = initializer.connect_database()
    handler.main()

    initializer.close_databse(conn)

except KeyboardInterrupt:
    print('\033[1;30mKeyboardInterrupt\033[m')
except EOFError:
    print('\033[1;30mEOFError\033[m')
