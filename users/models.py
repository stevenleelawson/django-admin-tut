from django.contrib.auth.models import AbstractUser
from django.db import models

class Permission(models.Model):
	name = models.CharField(max_length=200)

class Role(models.Model):
	# one user, one role but a role will have many permissions
	name = models.CharField(max_length=200)
	# when we create migrations, django will create another table for this relation
	permissions = models.ManyToManyField(Permission)

class User(AbstractUser):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200, unique=True)
	password = models.CharField(max_length=200)
	role =  models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
	username = None

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []