# Generated by Django 3.2.7 on 2021-09-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0004_auto_20210918_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primer',
            name='primer_sequence',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
