from django.db import models
import uuid

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('guest', 'Guest'),
#         ('host', 'Host'),
#         ('admin', 'Admin'),
#     )
#     user_id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#         unique=True
#     )

#     phone_number = models.CharField(
#         max_length=20,
#         null=True,
#         blank=True
#     )

#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='guest',
#         null=False,
#     )

#     created_at = models.DateTimeField(auto_now_add=True)


#     class Meta:
#         indexes = [
#             models.Index(fields=['email']),
#         ]

#     def __str__(self):
#         return self.email

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=120, null=False, unique=True, blank=False)
    password_hash = models.CharField(max_length=120, null=False, blank=False)
    phone_number = models.CharField(max_length=120, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='messages_sent')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    participants_id = models.ManyToManyField(
        User,
        related_name='conversations',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_emails = ", ".join(self.participants.values_list('email', flat=True)[:3])
        return f"Conversation ({participant_emails}...)"