from celery.task import task

@task()
def sample_task():
    return True