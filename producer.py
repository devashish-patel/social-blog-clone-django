from tasks import add, add_return, task_retry
from celery.result import AsyncResult

"""

add.delay(1, 2)

result = add_return.delay(5, 7)

while True:
    _result = AsyncResult(result.task_id)
    status = _result.status
    print (status)

    if 'SUCCESS' in status:
        print (_result.get())
        break

task_retry.delay()
"""