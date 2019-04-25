from django.db import models

# Create your models here.

class Order(models.Model):
    bee_name = models.CharField(max_length=240)
    ends_date = models.DateTimeField('Delivered Date')
    pickup_time_of_day = models.CharField(max_length=240)
    ends_time_of_day = models.CharField(max_length=240)
    store_address = models.CharField(max_length=250)
    drop_address = models.CharField(max_length=250)
    order_group = models.PositiveIntegerField()

    