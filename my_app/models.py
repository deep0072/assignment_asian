from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100)
class Plan(models.Model):
    name = models.CharField(max_length=100)
    features = models.ManyToManyField(Feature, related_name='plan_on_feature')

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)