from django.db import models

class Budget(models.Model):
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
    amount = models.IntegerField()
    user = models.CharField(max_length=255)