from django.db import models
from ads.models import Ad
from users.models import User

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, db_column='ad_id')
    walker = models.ForeignKey(User, on_delete=models.CASCADE, db_column='walker_id')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    
    class Meta:
        db_table = 'requests'
        managed = False
    
    def __str__(self):
        return f"Request by {self.walker.first_name} - {self.status}"


class Walk(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    ]
    
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, db_column='ad_id')
    walker = models.ForeignKey(User, on_delete=models.CASCADE, db_column='walker_id')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'walks'
        managed = False
    
    def __str__(self):
        return f"Walk for {self.ad.pet.name} - {self.status}"