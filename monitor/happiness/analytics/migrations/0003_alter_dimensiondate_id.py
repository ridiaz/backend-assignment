# Generated by Django 4.1.5 on 2023-01-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_alter_dimensionteam_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimensiondate',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
