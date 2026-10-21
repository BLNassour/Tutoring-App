from django.db import models
from django.contrib.auth.models import User

class TA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    bio = models.TextField()
    grades = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Availability(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    time_slot = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.ta.name} - {self.day}: {self.time_slot}"

class Signup(models.Model):
    fields = (
        'username',
        'email',
    )