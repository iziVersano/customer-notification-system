import uuid

from django.db import models


class Status(models.TextChoices):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class Job(models.Model):
    """One customer event becomes one job. Postgres holds its state."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Unique, so a redelivered event can't create a second job.
    event_id = models.CharField(max_length=100, unique=True)
    kind = models.CharField(max_length=50)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kind} {self.event_id} ({self.status})"


class Task(models.Model):
    """One step of a job, such as sending one notification."""

    # No index of its own: the (job, status) index below covers job lookups.
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="tasks", db_index=False
    )
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)
    attempts = models.PositiveIntegerField(default=0)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # finalize_job counts a job's tasks by status.
        indexes = [models.Index(fields=["job", "status"])]

    def __str__(self):
        return f"{self.name} ({self.status})"
