from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    email = models.EmailField()
    course = models.CharField(max_length=40)
    phone_no = models.BigIntegerField()

    def __str__(self):
        return self.name