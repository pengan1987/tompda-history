# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Orders(models.Model):
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    buyer = models.CharField(max_length=128, blank=True, null=True)
    seller = models.CharField(max_length=128, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
