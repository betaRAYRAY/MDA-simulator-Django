# Generated by Django 3.2.7 on 2021-09-23 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0020_alter_setting_chimerism_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='chimerism_model',
            field=models.CharField(choices=[('no_model', ''), ('A', 'model A'), ('B', 'model B'), ('C', 'model C')], max_length=10),
        ),
    ]