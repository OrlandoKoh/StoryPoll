import datetime

from django.db import models
from django.utils import timezone
from updown.fields import RatingField

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    def publish(self):
        self.pub_date = timezone.now()
        self.save()
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)
    rating = RatingField(can_change_vote=True)
    def __str__(self):
        return self.choice_text

class Reputation(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    rep = models.IntegerField(default=0)
    rating = RatingField(can_change_vote=True)
    def __str__(self):
        return self.rep
