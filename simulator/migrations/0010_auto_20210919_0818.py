# Generated by Django 3.2.7 on 2021-09-19 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0009_auto_20210918_2014'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.AlterField(
            model_name='sequence',
            name='sequence',
            field=models.TextField(blank=True, max_length=1000000),
        ),
    ]
