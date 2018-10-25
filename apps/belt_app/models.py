from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class UserManager(models.Manager):
    def validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = 'Your first name should only contain letters and be at least two characters.'

        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = 'Your last name should only contain letters and be at least two characters.'

        potential_matches = User.objects.filter(email=postData['email'])

        if len(potential_matches) > 0:
            errors['unique_email'] = 'Email already exists. Please provide a different email address.'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please enter a valid email address.'

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least eight characters.'

        if postData['password'] != postData['confirmpassword']:
            errors['passwords'] = 'Passwords do not match.'

        return errors


    def login_validator(self, postData):

        errors = {}
        if len(postData['lemail']) < 1:
            errors['no_email'] = 'This field is required.'

        if not EMAIL_REGEX.match(postData['lemail']):
            errors['email'] = 'Please enter a valid email address.'

        elif not User.objects.filter(email=postData['lemail']):
            errors['unique_email'] = 'No matching user.'

        if len(postData['lpassword']) < 1:
            errors['password'] = 'This field is required.'

        elif len(postData['lpassword']) < 1:
            errors['password'] = 'This field is required.'

            
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
