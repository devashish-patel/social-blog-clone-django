from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery.decorators import periodic_task
from celery.schedules import crontab
import redis
from datetime import timedelta

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task
def add(x, y):
    print ('{} + {} = {}'.format(x, y, x+y))


@app.task
def add_return(x, y):
    total = x + y
    return '{} + {} = {}'.format(x, y, total)


def backoff(attempts):
    return 2 ** attempts


@app.task(bind=True, max_retries=4, soft_time_limit=5)
def task_retry(self):
    try:
        for i in range(1, 11):
            print(i)

            if i == 5:
                raise ValueError()
    except SoftTimeLimitExceeded:
        print ("Boom")
    except ValueError as exe:
        print ("Exception at 5")
        raise self.retry(exc=exe, countdown=backoff(self.request.retries))


KEY = '4088587A2CAB44FD902D6D5C98CD2B17'


@periodic_task(bind=True, run_every=timedelta(seconds=1), name='task_send_email')
def send_emails(self):
    """
    Mutual Exclusion: Only one worker can get the task so we'll apply some locking
    mechanism
    """
    REDIS_CLIENT = redis.Redis()
    timeout = 60 * 5  # 5 min
    have_lock = False
    my_lock = REDIS_CLIENT.lock(KEY, timeout=timeout)

    try:
        # This is critical section: only one worker can get it at one time
        have_lock = my_lock.acquire(blocking=False)
        print ('Lock Acquired!')
        if have_lock:
            mail = "example.mail"
            print ("{0} has sent email to: {1}".format(self.request.hostname,
                                                       mail))
    finally:
        if have_lock:
            my_lock.release()
            print ('Lock Released!')