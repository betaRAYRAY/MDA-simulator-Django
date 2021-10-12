from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields import BooleanField
from django.db.models.fields.json import JSONField

# Create your models here.

## input data ##

class Sequence(models.Model):
    name = models.CharField(max_length=200)
    sequence = models.TextField()

class Primer(models.Model):
    name = models.CharField(max_length=200)
    active = BooleanField()
    direction = BooleanField()
    sequence = models.CharField(max_length=500)
    mismatch_score = models.IntegerField()

class Setting(models.Model):
    number_of_products = models.IntegerField()
    number_of_products_EACHONCE = BooleanField()
    global_termination_probability = models.FloatField()
    local_termination_probability = models.FloatField()

    # model choices
    CHOICES = (
        ('no_model', ''),
        ('A', 'model A'),
        ('B', 'model B'),
        ('C', 'model C')
    )

    chimerism_model = models.CharField(max_length=10, choices=CHOICES)
    chimerism_probability = models.FloatField()

## result data ##

class AnnealedPrimer(models.Model):
    primer = models.ForeignKey('Primer', on_delete=models.CASCADE)
    start = models.IntegerField()
    end = models.IntegerField()

class PrimerProduct(models.Model):
    forward_primer = models.ForeignKey('AnnealedPrimer', on_delete=models.CASCADE, related_name='forward_primer')
    reverse_primer = models.ForeignKey('AnnealedPrimer', on_delete=models.CASCADE, related_name='reverse_primer')
 
class ResultProduct(models.Model):
    primer_product = models.ForeignKey('PrimerProduct', on_delete=models.CASCADE, related_name='primer_product')
    stop = models.IntegerField()    # -1 -> no stop
    direction = BooleanField()

class ChimericResultProduct(models.Model):
    primer_product_1 = models.ForeignKey('PrimerProduct', on_delete=models.CASCADE, related_name='primer_product_1')
    primer_product_2 = models.ForeignKey('PrimerProduct', on_delete=models.CASCADE, related_name='primer_product_2')
    stop_1 = models.IntegerField()
    stop_2 = models.IntegerField()

class ResultString(models.Model):
    product_string = models.CharField(max_length=1000)

class ResultSequenceString(models.Model):
    product_string = models.CharField(max_length=100000)