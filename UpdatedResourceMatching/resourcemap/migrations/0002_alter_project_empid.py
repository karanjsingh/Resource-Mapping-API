# Generated by Django 3.2.5 on 2022-12-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='empid',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
