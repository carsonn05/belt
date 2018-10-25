from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from apps.belt_app.models import *


class TripManager(models.Manager):
    def validator(self, postData):

        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = 'This field is required.'

        if len(postData['description']) < 1:
            errors['description'] = 'This field is required.'

        if len(postData['start_date']) < 1:
            errors['start_date'] = 'This field is required.'

        elif postData['start_date'] < str(datetime.now()):
            errors['start_date'] = 'Start date should be a future date.'

        if len(postData['end_date']) < 1:
            errors['end_date'] = 'This field is required.'

        elif postData['end_date'] < str(datetime.now()):
            errors['end_date'] = 'End date should be a future date.'

        if postData['start_date'] > postData['end_date']:
            errors['start_date'] = 'Start date must be before the end date.'


        return errors



class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name = 'owner', on_delete='models.CASCADE')
    traveler = models.ManyToManyField(User, related_name = 'trips')
    objects = TripManager()

