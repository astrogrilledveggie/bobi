from django.db import models


class Userinput(models.Model):
    userinput_text = models.CharField(null=True, blank=True, max_length=300)
    user = models.CharField(max_length=255)

class Botmessage(models.Model):
    userinput = models.OneToOneField(Userinput, on_delete=models.CASCADE)
    botmessage_text = models.CharField(null=True, blank=True, max_length=300)
    user = models.CharField(max_length=255, default="gaby")

def __str__(self):
    return str(self.id)