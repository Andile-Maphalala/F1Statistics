# Generated by Django 3.2.4 on 2021-07-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Head2Head', '0003_fasteslapclass_resultclass_startingclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fasteslapclass',
            name='Pos',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='resultclass',
            name='Pos',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='startingclass',
            name='Pos',
            field=models.CharField(max_length=200),
        ),
    ]
