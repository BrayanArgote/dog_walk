from django.db import models
from users.models import User

class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner_id')
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'pets'
        managed = False
    
    def __str__(self):
        return f"{self.name} ({self.type})"