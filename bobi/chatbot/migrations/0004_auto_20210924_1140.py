# Generated by Django 3.2.7 on 2021-09-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_auto_20210923_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessage',
            name='botmessage_text',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userinput',
            name='userinput_text',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
