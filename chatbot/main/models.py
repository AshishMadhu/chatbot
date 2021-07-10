from django.db import models

# Create your models here.

class ResponseCount(models.Model):
    telegram = 'telegram'
    ws = 'ws'
    choices = ([telegram, 'Telegram'], [ws, 'Websocket'])
    source = models.CharField(max_length=10, choices=choices)
    stupid_count = models.PositiveIntegerField(default = 0)
    fat_count = models.PositiveIntegerField(default = 0)
    dumb_count = models.PositiveIntegerField(default = 0)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.source}: stupid-{self.stupid_count} fat-{self.fat_count} dumb- {self.dumb_count}"
        