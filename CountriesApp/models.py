from django.db import models


# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)


class Language(models.Model):
    name = models.CharField(max_length=100)


class countries_languages(models.Model):
    country_name = models.CharField(max_length=100)
    language_name = models.CharField(max_length=100)
