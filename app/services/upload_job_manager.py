"""
upload_job_manager.py

Manages background upload jobs, progress,
status, errors, and cancellation requests.
"""

from dataclasses import dataclass
from threading import Lock
from uuid import uuid4


# ==============================================================
# UPLOAD JOB
# ==============================================================

@dataclass
class UploadJob:
    """
    Represents one background upload job.
    """

    job_id: str

    filename: str

    progress: int = 0

    stage: str = "Waiting to start..."

    status: str = "queued"

    error: str | None = None


# ==============================================================
# UPLOAD JOB MANAGER
# ==============================================================

class UploadJobManager:
    """
    Stores and manages background upload jobs.
    """

    def __init__(self):

        self.jobs: dict[str, UploadJob] = {}

        self.lock = Lock()

    # ==========================================================
    # CREATE JOB
    # ==========================================================

    def create_job(
        self,
        filename: str,
    ) -> UploadJob:
        """
        Create a new upload job.

        The job ID is generated automatically.
        """

        job_id = str(
            uuid4()
        )

        job = UploadJob(
            job_id=job_id,
            filename=filename,
        )

        with self.lock:

            self.jobs[job_id] = job

        return job

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        job_id: str,
        filename: str,
    ) -> UploadJob:
        """
        Create a job using an explicitly supplied job ID.

        Kept for compatibility with other code.
        """

        job = UploadJob(
            job_id=job_id,
            filename=filename,
        )

        with self.lock:

            self.jobs[job_id] = job

        return job

    # ==========================================================
    # GET JOB
    # ==========================================================

    def get_job(
        self,
        job_id: str,
    ) -> UploadJob | None:
        """
        Get a job by its ID.
        """

        with self.lock:

            return self.jobs.get(
                job_id
            )

    # ==========================================================
    # GET
    # ==========================================================

    def get(
        self,
        job_id: str,
    ) -> UploadJob | None:
        """
        Alias for get_job().
        """

        return self.get_job(
            job_id
        )

    # ==========================================================
    # UPDATE JOB
    # ==========================================================

    def update(
        self,
        job_id: str,
        progress: int | None = None,
        stage: str | None = None,
        status: str | None = None,
        error: str | None = None,
    ) -> None:
        """
        Update the state of an upload job.
        """

        with self.lock:

            job = self.jobs.get(
                job_id
            )

            if job is None:
                return

            if progress is not None:

                job.progress = max(
                    0,
                    min(
                        100,
                        progress,
                    ),
                )

            if stage is not None:

                job.stage = stage

            if status is not None:

                job.status = status

            if error is not None:

                job.error = error

    # ==========================================================
    # START
    # ==========================================================

    def start(
        self,
        job_id: str,
    ) -> None:
        """
        Mark a job as processing.
        """

        self.update(
            job_id=job_id,
            progress=1,
            stage="Starting upload...",
            status="processing",
        )

    # ==========================================================
    # CANCEL
    # ==========================================================

    def cancel(
        self,
        job_id: str,
    ) -> bool:
        """
        Request cancellation of a job.
        """

        with self.lock:

            job = self.jobs.get(
                job_id
            )

            if job is None:
                return False

            # Already completed.
            if job.status == "completed":

                return False

            # Already failed.
            if job.status == "failed":

                return False

            # Already cancelled.
            if job.status == "cancelled":

                return True

            job.status = "cancelled"

            job.stage = "Cancellation requested."

            return True

    # ==========================================================
    # IS CANCELLED
    # ==========================================================

    def is_cancelled(
        self,
        job_id: str,
    ) -> bool:
        """
        Check whether a cancellation was requested.
        """

        with self.lock:

            job = self.jobs.get(
                job_id
            )

            if job is None:

                return False

            return (
                job.status == "cancelled"
            )

    # ==========================================================
    # COMPLETE
    # ==========================================================

    def complete(
        self,
        job_id: str,
    ) -> None:
        """
        Mark a job as completed.
        """

        with self.lock:

            job = self.jobs.get(
                job_id
            )

            if job is None:
                return

            # Never overwrite cancellation.
            if job.status == "cancelled":

                return

            job.status = "completed"

            job.progress = 100

            job.stage = "Upload completed."

            job.error = None

    # ==========================================================
    # FAIL
    # ==========================================================

    def fail(
        self,
        job_id: str,
        error: str,
    ) -> None:
        """
        Mark a job as failed.
        """

        with self.lock:

            job = self.jobs.get(
                job_id
            )

            if job is None:
                return

            # Never overwrite cancellation.
            if job.status == "cancelled":

                return

            job.status = "failed"

            job.stage = "Upload failed."

            job.error = error

    # ==========================================================
    # REMOVE
    # ==========================================================

    def remove(
        self,
        job_id: str,
    ) -> None:
        """
        Remove a job from memory.
        """

        with self.lock:

            self.jobs.pop(
                job_id,
                None,
            )

    # ==========================================================
    # ALL JOBS
    # ==========================================================

    def all(
        self,
    ) -> list[UploadJob]:
        """
        Return all jobs.
        """

        with self.lock:

            return list(
                self.jobs.values()
            )


# ==============================================================
# GLOBAL JOB MANAGER
# ==============================================================

upload_job_manager = UploadJobManager()