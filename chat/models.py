from django.db import models
from django.conf import settings

class Dialog(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dialog_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dialog_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Dialog between {self.user1.email} and {self.user2.email}"

class Message(models.Model):
    dialog = models.ForeignKey(Dialog, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.timestamp}"
