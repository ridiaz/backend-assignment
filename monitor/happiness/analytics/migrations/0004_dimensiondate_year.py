# Generated by Django 4.1.5 on 2023-01-23 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_alter_dimensiondate_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimensiondate',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]