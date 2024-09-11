from django.db import models

# Create your models here.
class Location(models.Model):
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    timezone = models.CharField(max_length=10)

class Picture(models.Model):
    large = models.URLField(max_length=255)
    medium = models.URLField(max_length=255)
    thumbnail = models.URLField(max_length=255)

class Student(models.Model):
    gender = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    dob = models.DateField()
    registered = models.DateTimeField()
    phone = models.CharField(max_length=20)
    id_name = models.CharField(max_length=20)
    id_value = models.CharField(max_length=50)
    nat = models.CharField(max_length=10)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    picture = models.OneToOneField(Picture, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class User(models.Model):
    username = models.CharField(max_length=50)
    salt = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=256)

    class Meta:
        db_table = 'users'