# Generated by Django 3.2.23 on 2023-12-24 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_the_best',
            field=models.BooleanField(default=False),
        ),
    ]
