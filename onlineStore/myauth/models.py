from django.contrib.auth.models import User
from django.db import models


class Dialog(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs_user2')

    def get_partner_for(self, user):
        if user == self.user1:
            return self.user2
        elif user == self.user2:
            return self.user1


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
