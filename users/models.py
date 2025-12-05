from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('walker', 'Walker'),
    ]
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField()
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'users'
        managed = False
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"