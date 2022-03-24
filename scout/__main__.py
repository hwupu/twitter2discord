import sys

if sys.version_info.major < 3:
    print('\033[1;31mNeeds Python3 to run.\033[m')
    exit(1)

import argparse
import logging
import os

from . import database
from . import handler

def parse_cmd_args():
    argparser = argparse.ArgumentParser()
    help_msg = """Fetch tweets images and post to Discord"""

    argparser.add_argument("-r",
                           dest="repeat",
                           action="store_true",
                           default=False,
                           help=("Repeat every 15 minutes"))

    argparser.add_argument("--debug",
                           dest="debug",
                           action="store_true",
                           default=False,
                           help=("print all info and warning messages"))
    return argparser


def main():
    try:
        database.connect()
        handler.main()
    except KeyboardInterrupt:
        print('\033[1;30mKeyboardInterrupt\033[m')
    except EOFError:
        print('\033[1;30mEOFError\033[m')
    finally:
        database.close()


args_dict = vars(parse_cmd_args().parse_args())

if not args_dict.get("repeat"):
    main()
    exit()

logger = logging.getLogger()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))

if args_dict.get("debug"):
    logger.setLevel(logging.DEBUG)


import schedule
import signal
import time

alive = True

def stop(self, *args):
    initializer.close_databse(conn)
    schedule.clear()

    global alive
    alive = False

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

schedule.every(15).minutes.do(main)
schedule.run_all()

print('Start polling Twitters from watchlist every 15 minutes...')

while alive:
    schedule.run_pending()
    time.sleep(1)


