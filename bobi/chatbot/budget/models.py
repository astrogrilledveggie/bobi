from django.db import models
import datetime

class Budget(models.Model):
    Dining = 'Dining'
    Groceries = 'Groceries'
    Bill = 'Bill'
    Transport = 'Transport'
    Shopping = 'Shopping'
    Others = 'Others'
    category_choices = [
        (Dining, 'Dining'),
        (Groceries, 'Groceries'),
        (Bill, 'Bill'),
        (Transport, 'Transport'),
        (Shopping, 'Shopping'),
        (Others, 'Others'),
    ]

    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, choices=category_choices, default=Others,)
    details = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.CharField(max_length=255)