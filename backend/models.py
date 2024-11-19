from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Event(models.Model):
    date = models.DateField()
    time = models.TimeField()
    court_number = models.IntegerField()
    week_number = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('playing', 'Playing'), ('standby', 'Standby')],
        default='standby'
    )

    class Meta:
        ordering = ['timestamp']

    def clean(self):
        # Check if user has already voted 3 times this week
        week_number = self.event.week_number
        year = self.event.year
        user_votes = Vote.objects.filter(
            user=self.user,
            event__week_number=week_number,
            event__year=year
        ).count()
        
        if user_votes >= 3:
            raise ValidationError('Maximum 3 votes per week allowed') 