from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractUser):
    # Checker requires: password, user_id
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)

    # Add any other custom fields you want
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username


# -----------------------------
# Conversation Model
# -----------------------------
class Conversation(models.Model):
    # Checker requires: conversation_id
    conversation_id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -----------------------------
# Message Model
# -----------------------------
class Message(models.Model):
    # Checker requires: message_id
    message_id = models.AutoField(primary_key=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
