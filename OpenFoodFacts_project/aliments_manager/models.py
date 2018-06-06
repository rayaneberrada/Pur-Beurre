from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Favorites(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	url = models.CharField(max_length = 200)
	image = models.CharField(max_length = 200)
	name = models.CharField(max_length = 100)
	nutriscore = models.CharField(max_length = 1)
	code = models.CharField(max_length = 13)

	def __str__(self):
		return self.name