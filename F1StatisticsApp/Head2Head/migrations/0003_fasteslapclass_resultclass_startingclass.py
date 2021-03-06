# Generated by Django 3.2.4 on 2021-07-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Head2Head', '0002_driverclass_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='FastesLapClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pos', models.IntegerField(default=0)),
                ('No', models.CharField(max_length=200)),
                ('Driver', models.CharField(max_length=200)),
                ('Car', models.CharField(max_length=200)),
                ('Lap', models.IntegerField(default=0)),
                ('TOD', models.CharField(max_length=200)),
                ('Time', models.CharField(max_length=200)),
                ('AVGSpeed', models.FloatField(default=0)),
                ('GP', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ResultClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pos', models.IntegerField(default=0)),
                ('No', models.CharField(max_length=200)),
                ('Driver', models.CharField(max_length=200)),
                ('Car', models.CharField(max_length=200)),
                ('Laps', models.IntegerField(default=0)),
                ('Time', models.CharField(max_length=200)),
                ('Pts', models.IntegerField(default=0)),
                ('GP', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StartingClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pos', models.IntegerField(default=0)),
                ('No', models.CharField(max_length=200)),
                ('Driver', models.CharField(max_length=200)),
                ('Car', models.CharField(max_length=200)),
                ('Time', models.CharField(max_length=200)),
                ('GP', models.CharField(max_length=200)),
            ],
        ),
    ]
