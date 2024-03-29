# Generated by Django 3.2.5 on 2022-12-20 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=200)),
                ('taskname', models.CharField(max_length=200)),
                ('empid', models.CharField(max_length=200)),
                ('starttime', models.DateField()),
                ('endtime', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.CharField(max_length=200)),
                ('skill', models.CharField(max_length=200)),
                ('availstartdate', models.DateField()),
                ('availenddate', models.DateField()),
            ],
        ),
    ]
