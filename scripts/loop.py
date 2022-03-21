
import schedule
import signal
import time

alive = True

def job1():
    print('job')


def stop(self, *args):
    global alive
    alive = False
    schedule.clear()


def main():
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    schedule.every(1).seconds.do(job1) 

    while alive:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
