# Generated by Django 3.2.7 on 2021-09-18 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0006_auto_20210918_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_file', models.FileField(blank=True, upload_to='')),
                ('primer_file', models.FileField(blank=True, upload_to='')),
            ],
        ),
    ]
