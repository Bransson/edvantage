# Generated by Django 3.2 on 2024-10-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20241024_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagetasks',
            name='datetime',
            field=models.DateField(auto_now=True),
        ),
    ]