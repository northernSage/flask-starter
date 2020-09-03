import logging
from time import sleep

from app import create_app
from app import db
from app.models import Task
from rq import get_current_job

app = create_app()
app.app_context().push()

# custom logger
logger = logging.getLogger("task_logger")
logger.setLevel(logging.ERROR)
fh = logging.FileHandler("log.txt")
fh.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def _set_task_progress(progress, job, job_id):
    """helper function for task progress update"""
    if job:
        job.meta["progress"] = progress
        job.save_meta()
        if int(progress) >= 100:
            task = Task.query.filter_by(id=job_id).first()
            task.complete = True
            db.session.commit()


def test_task(delay):
    """simple task for testing purposes"""
    job = get_current_job()
    job_id = job.get_id()
    try:
        for i in range(5):
            sleep(int(delay))
            _set_task_progress(i * 100 / 5, job, job_id)
    except Exception as e:
        logger.error(str(e))
    else:
        _set_task_progress(100.0, job, job_id)


if __name__ == "__main__":
    test_task()
