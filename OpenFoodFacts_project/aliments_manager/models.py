from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Favorites(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	url = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)
	nutriscore = models.CharField(max_length = 1)
	code = models.CharField(max_length = 15, default = "0122")

	def __str__(self):
		return self.name