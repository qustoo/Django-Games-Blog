from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

    def __str__(self):
        return f"Group {self.name} - {self.members}"

    def get_absolute_url(self):
        return reverse("chat:group_detail", kwargs={"pk": self.uuid})

    def add_user_to_group(self, user):
        self.members.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()

    def remove_user_from_group(self, user: User):
        self.members.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(
        Group, related_name="group_messages", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        date = self.created_at.date()
        time = self.created_at.time()
        return f"{self.author}:- {self.content} @{date} {time.hour}:{time.minute}"


class Event(models.Model):
    CHOICES = [("Join", "join"), ("Left", "left")]
    type = models.CharField(choices=CHOICES, max_length=4)
    description = models.CharField(
        help_text="A description of the event that occurred",
        max_length=100,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        Group, related_name="group_events", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.description

    def save(self, *args, **kwargs):
        # сохраняем описание, тип события и группу
        self.description = f"{self.user} {self.type} the {self.group.name} group"
        super().save(*args, **kwargs)
