import traceback

import celery
from django.utils import timezone
from .apis import post_or_put_celery_log


class TaskLogger(celery.Task):
    def __call__(self, *args, **kwargs):
        log = {
            "task_id": self.request.id,
            "task_name": self.name,
            "periodic_task_name": (
                self.request.get("periodic_task_name")[:255]
                if self.request.get("periodic_task_name")
                else None
            ),
            "args": args or None,
            "kwargs": kwargs or None,
            "context": self.request.__dict__,
            "started_at": timezone.now().timestamp(),
        }
        post_or_put_celery_log(log, "POST")
        error = None
        updated_log = {"task_id": self.request.id}
        to_return = None
        try:
            to_return = super().__call__(*args, **kwargs)
        except Exception as e:
            updated_log["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
            error = e
        finally:
            updated_log["ended_at"] = timezone.now().timestamp()
            post_or_put_celery_log(updated_log, "PUT")
            if error:
                raise error
        return to_return
