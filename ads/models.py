from django.db import models
from pets.models import Pet

class Ad(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]
    
    id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='pet_id')
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    place = models.CharField(max_length=50)
    text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=13, choices=STATUS_CHOICES)
    
    class Meta:
        db_table = 'ads'
        managed = False
    
    def __str__(self):
        return f"Ad for {self.pet.name} on {self.date}"